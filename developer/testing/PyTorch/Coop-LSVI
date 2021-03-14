Input: T, φ, H, S, sequence βh = {(β
t
m,h)m,t}.
2: Initialize: S
t
m,h, δS
t
m,h = 0, U
m
h , Wm
h = ∅.
3: for episode t = 1, 2, ..., T do
4: for agent m ∈ M do
5: Receive initial state x
t
m,1.
6: Set V
t
m,H+1(·) ← 0.
7: for step h = H, ..., 1 do
8: Compute Λ
t
m,h ← S
t
m,h + δS
t
m,h.
9: Compute Qbt
m,h and σ
t
m,h (Eqns. 5 and 6).
10: Compute Q
t
m,h(·, ·) (Eqn. 1)
11: Set V
t
m,h(·) ← maxa∈A Q
t
m,h(·, a).
12: end for
13: for step h = 1, ..., H do
14: Take action a
t
m,h ← arg maxa∈A Q
t
m,h(x
t
m,h, a).
15: Observe r
t
m,h, xt
m,h+1.
16: Update δS
t
m,h ← δS
t
m,h + φ(z
t
m,h)φ(z
t
m,h)
⊤.
17: Update Wm
h ← Wm
h ∪ (m, x, a, x′
).
18: if log det(S
t
m,h+δS
t
m,h+λI)
det
St
m,h+λI
 >
S
∆tm,h
then
19: Synchronize← True.
20: end if
21: end for
22: end for
23: if Synchronize then
24: for step h = H, ..., 1 do
25: [∀ Agents] Send Wh
m →Server.
26: [Server] Aggregate Wh → ∪m∈MWm
h .
27: [Server] Communicate Wh
to each agent.
28: [∀ Agents] Set δS
t
h ← 0, Wm
h ← ∅.
29: [∀ Agents] Set S
t
h ← S
t
h +
P
z∈Wh φ(z)φ(z)
⊤.
30: [∀ Agents] Set U
m
h ← Um
h ∪ Wm
h
31: end for
32: end if
33: end for
