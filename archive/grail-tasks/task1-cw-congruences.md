# Task: Chevalley-Warning Congruence System

Read these files first:
- ~/claude/multi-agent/seeds/grail-briefing.md (full problem context)
- ~/claude/multi-agent/claude-023-postmortem (insights from prior run)

Your task: determine whether Chevalley-Warning congruences, combined with the assumption N_p = 0, yield a contradiction.

## Setup

For G = C_p^4 (cyclic group of order p, rank 4), exponent q = p. A sequence S of length l = 17(p-1) with each of 17 distinct nonzero elements appearing p-1 times.

D*(G) = 4(p-1)+1.

Grynkiewicz Proposition 3.2 gives: for alpha=0, m=0:
Sum_{j>=0} (p-1)^{jp} * C(j,i) * N_{jp}(S) ≡ 0 mod p
for i = 0, ..., t-1, where t satisfies: l >= tp - 1 + D*(G).

So 17(p-1) >= tp - 1 + 4p - 3, giving t <= 13 - 13/p.

Key simplification: (p-1)^{jp} = (-1)^{jp} = (-1)^j mod p (since p is odd).

So the system becomes:
For i=0,...,t-1: Sum_{j>=1} C(j,i)*(-1)^j * N_{jp} ≡ -1 (i=0) or 0 (i>0) mod p

With N_0 = 1, and we assume N_p = 0.

Unknowns: N_{2p}, N_{3p}, ..., N_{kp} where k = floor(l/p) = floor(17(p-1)/p).

## Your computation

Write Python code to:
1. For p = 5, 7, 11, 13, 17, 19, 23:
   a. Compute t (number of equations) and k (number of unknowns including N_p=0)
   b. Build coefficient matrix A[i][j] = C(j+2, i) * (-1)^(j+2) mod p (for j indexing N_{2p}, N_{3p}, ...)
   c. RHS vector: b[0] = -1 - C(1,0)*(-1)^1*0 = -1 mod p; b[i] = 0 for i>0
   d. Check rank of A vs rank of [A|b] over F_p. If rank [A|b] > rank A, system is INCONSISTENT → N_p > 0 is forced!

2. Verify: for G = C_p^2 (Kemnitz), l = 4p-3, D* = 2(p-1)+1. The system should give 3 equations in 3 unknowns and be inconsistent when N_p = 0. This reproduces Reiher's result.

3. For each p where the rank-4 system is NOT inconsistent: find the null space. What solutions (N_{2p}, N_{3p}, ...) are compatible with N_p = 0? Are they physically meaningful (non-negative integers)?

4. Try higher m values (m=1 gives congruences mod p^2). Does this help?

Save all results to ~/claude/grail-tasks/results-cw-congruences.txt
