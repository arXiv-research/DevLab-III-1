#!/bin/sh
REPO="https://raw.githubusercontent.com/paritytech/parity-ethereum/master/ethcore/res/ethereum"
CHAIN_H=../src/verifier/eth1/nano/chains.h

echo "// defines the chainspecs as rlp encoded values for different chains"  > $CHAIN_H
echo "// this file is autogenerated with the update_chainspec.sh script. Please don't edit it!\n"  >> $CHAIN_H
curl -s $REPO/foundation.json | in3 chainspec -name MAINNET >> $CHAIN_H
curl -s $REPO/goerli.json     | in3 chainspec -name GOERLI  >> $CHAIN_H
