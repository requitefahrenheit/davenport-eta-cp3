# Task: Grynkiewicz Weighted CW Applied to the Grail

Read these files first:
- ~/claude/multi-agent/seeds/grail-briefing.md (full problem context)
- ~/claude/multi-agent/claude-023-postmortem (insights from prior run)

The post-mortem's #1 recommendation: use WEIGHTED Chevalley-Warning (Grynkiewicz Theorem 1.3) with weight functions to get additional independent congruences.

## Background

Grynkiewicz (2023) Theorem 1.3 allows weight functions w_j(X) in the CW congruence. With weight w_i(X) = X^i (binomial coefficient basis), each weight gives an INDEPENDENT congruence.

Reiher's Kemnitz proof used this: with alpha=0 and weights w_0=1, w_1=X, w_2=C(X,2), he got 3 congruences on N_p, N_{2p}, N_{3p}. With N_p=0 assumed, the system of 3 equations in 2 unknowns was overdetermined and inconsistent for p >= 3.

For our problem (rank 4, n=18 vectors, l=17(p-1)):
- Standard CW (m=0, varying t) gives ~13 equations
- But there are ~13 unknowns (N_{2p} through N_{13p})
- System is square, likely consistent

The weighted version gives ADDITIONAL equations by using higher weight functions.

## Your computation

Recreate Reiher's proof for C_p^2 first (verify the method works):
1. Set G = C_p^2, l = 4p-3, D* = 2(p-1)+1, alpha = 0
2. Apply Proposition 3.2 with t=1, m=0 and weights w_0(X)=1, w_1(X)=X
3. Show the system is inconsistent when N_p = 0

Then apply to G = C_p^4, l = 17(p-1):
4. Compute ALL congruences from Proposition 3.2 with:
   - alpha = 0 (zero-sums of length divisible by p)
   - alpha = p-1 (length congruent to p-1 mod p) 
   - Different m values (0, 1)
   - Different weight functions w_i(X) = C(X, i) for i = 0, 1, 2, ...
5. How many INDEPENDENT congruences can we extract?
6. How many unknowns remain after setting N_p = 0?
7. Is the system overdetermined? Is it inconsistent?

Also try: what if we additionally assume N_{2p} = 0? The rank-3 theorem says that any collinear triple produces a zero-sum of weight <= p. If we can show that SOME N_j must be nonzero, and that forces other N_j's to be nonzero via the congruences, we might get a cascade.

IMPORTANT: The weight function w(X) = C(X, i) has degree i. The variable count condition in Theorem 1.3 is:
n > (m-1)*max{1, phi(q_j)/(p-1) * deg f_j} + Sum (t_i+1)*p^{m_i-1}/(p-1) * deg f_i

where t_i = deg w_i. Higher-degree weights require more variables, so there's a tradeoff.

Compute the exact bound for each weight degree and determine the maximum number of independent congruences.

Save results to ~/claude/grail-tasks/results-weighted-cw.txt
