package relay_test

import (
	"context"
	"net"
	"strings"
	"sync"
	"testing"
	"time"

	cienv "github.com/jbenet/go-cienv"
	libp2p "github.com/libp2p/go-libp2p"
	relay "github.com/libp2p/go-libp2p/p2p/host/relay"

	cid "github.com/ipfs/go-cid"
	circuit "github.com/libp2p/go-libp2p-circuit"
	"github.com/libp2p/go-libp2p-core/event"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/network"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/libp2p/go-libp2p-core/routing"
	ma "github.com/multiformats/go-multiaddr"
	manet "github.com/multiformats/go-multiaddr/net"
)

// test specific parameters
func init() {
	relay.BootDelay = 1 * time.Second
	relay.AdvertiseBootDelay = 100 * time.Millisecond
}

// mock routing
type mockRoutingTable struct {
	mx        sync.Mutex
	providers map[string]map[peer.ID]peer.AddrInfo
	peers     map[peer.ID]peer.AddrInfo
}

type mockRouting struct {
	h   host.Host
	tab *mockRoutingTable
}

func newMockRoutingTable() *mockRoutingTable {
	return &mockRoutingTable{providers: make(map[string]map[peer.ID]peer.AddrInfo)}
}

func newMockRouting(h host.Host, tab *mockRoutingTable) *mockRouting {
	return &mockRouting{h: h, tab: tab}
}

func (m *mockRouting) FindPeer(ctx context.Context, p peer.ID) (peer.AddrInfo, error) {
	m.tab.mx.Lock()
	defer m.tab.mx.Unlock()
	pi, ok := m.tab.peers[p]
	if !ok {
		return peer.AddrInfo{}, routing.ErrNotFound
	}
	return pi, nil
}

func (m *mockRouting) Provide(ctx context.Context, cid cid.Cid, bcast bool) error {
	m.tab.mx.Lock()
	defer m.tab.mx.Unlock()

	pmap, ok := m.tab.providers[cid.String()]
	if !ok {
		pmap = make(map[peer.ID]peer.AddrInfo)
		m.tab.providers[cid.String()] = pmap
	}

	pi := peer.AddrInfo{ID: m.h.ID(), Addrs: m.h.Addrs()}
	pmap[m.h.ID()] = pi
	if m.tab.peers == nil {
		m.tab.peers = make(map[peer.ID]peer.AddrInfo)
	}
	m.tab.peers[m.h.ID()] = pi

	return nil
}

func (m *mockRouting) FindProvidersAsync(ctx context.Context, cid cid.Cid, limit int) <-chan peer.AddrInfo {
	ch := make(chan peer.AddrInfo)
	go func() {
		defer close(ch)
		m.tab.mx.Lock()
		defer m.tab.mx.Unlock()

		pmap, ok := m.tab.providers[cid.String()]
		if !ok {
			return
		}

		for _, pi := range pmap {
			select {
			case ch <- pi:
			case <-ctx.Done():
				return
			}
		}
	}()

	return ch
}

// connector
func connect(t *testing.T, a, b host.Host) {
	pinfo := peer.AddrInfo{ID: a.ID(), Addrs: a.Addrs()}
	err := b.Connect(context.Background(), pinfo)
	if err != nil {
		t.Fatal(err)
	}
}

// and the actual test!
func TestAutoRelay(t *testing.T) {
	if cienv.IsRunning() {
		t.Skip("disabled on CI: fails 99% of the time")
	}

	manet.Private4 = []*net.IPNet{}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	mtab := newMockRoutingTable()
	makeRouting := func(h host.Host) (routing.PeerRouting, error) {
		mr := newMockRouting(h, mtab)
		return mr, nil
	}

	h1, err := libp2p.New(ctx, libp2p.EnableRelay())
	if err != nil {
		t.Fatal(err)
	}
	// announce dns addrs because filter out private addresses from relays,
	// and we consider dns addresses "public".
	_, err = libp2p.New(ctx,
		libp2p.EnableRelay(circuit.OptHop),
		libp2p.EnableAutoRelay(),
		libp2p.Routing(makeRouting),
		libp2p.AddrsFactory(func(addrs []ma.Multiaddr) []ma.Multiaddr {
			for i, addr := range addrs {
				saddr := addr.String()
				if strings.HasPrefix(saddr, "/ip4/127.0.0.1/") {
					addrNoIP := strings.TrimPrefix(saddr, "/ip4/127.0.0.1")
					addrs[i] = ma.StringCast("/dns4/localhost" + addrNoIP)
				}
			}
			return addrs
		}))
	if err != nil {
		t.Fatal(err)
	}
	h3, err := libp2p.New(ctx, libp2p.EnableRelay(), libp2p.EnableAutoRelay(), libp2p.Routing(makeRouting))
	if err != nil {
		t.Fatal(err)
	}
	h4, err := libp2p.New(ctx, libp2p.EnableRelay())
	if err != nil {
		t.Fatal(err)
	}

	// verify that we don't advertise relay addrs initially
	for _, addr := range h3.Addrs() {
		_, err := addr.ValueForProtocol(circuit.P_CIRCUIT)
		if err == nil {
			t.Fatal("relay addr advertised before auto detection")
		}
	}

	// connect to AutoNAT, have it resolve to private.
	connect(t, h1, h3)
	time.Sleep(300 * time.Millisecond)
	privEmitter, _ := h3.EventBus().Emitter(new(event.EvtLocalReachabilityChanged))
	privEmitter.Emit(event.EvtLocalReachabilityChanged{Reachability: network.ReachabilityPrivate})
	// Wait for detection to do its magic
	time.Sleep(3000 * time.Millisecond)

	// verify that we now advertise relay addrs (but not unspecific relay addrs)
	unspecificRelay, err := ma.NewMultiaddr("/p2p-circuit")
	if err != nil {
		t.Fatal(err)
	}

	haveRelay := false
	for _, addr := range h3.Addrs() {
		if addr.Equal(unspecificRelay) {
			t.Fatal("unspecific relay addr advertised")
		}

		_, err := addr.ValueForProtocol(circuit.P_CIRCUIT)
		if err == nil {
			haveRelay = true
		}
	}

	if !haveRelay {
		t.Fatal("No relay addrs advertised")
	}

	// verify that we can connect through the relay
	var raddrs []ma.Multiaddr
	for _, addr := range h3.Addrs() {
		_, err := addr.ValueForProtocol(circuit.P_CIRCUIT)
		if err == nil {
			raddrs = append(raddrs, addr)
		}
	}

	err = h4.Connect(ctx, peer.AddrInfo{ID: h3.ID(), Addrs: raddrs})
	if err != nil {
		t.Fatal(err)
	}

	// verify that we have pushed relay addrs to connected peers
	haveRelay = false
	for _, addr := range h1.Peerstore().Addrs(h3.ID()) {
		if addr.Equal(unspecificRelay) {
			t.Fatal("unspecific relay addr advertised")
		}

		_, err := addr.ValueForProtocol(circuit.P_CIRCUIT)
		if err == nil {
			haveRelay = true
		}
	}

	if !haveRelay {
		t.Fatal("No relay addrs pushed")
	}
}
