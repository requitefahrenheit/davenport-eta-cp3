# Task: Direct Proof Attempt for the Grail

Read these files carefully:
- ~/claude/multi-agent/seeds/grail-briefing.md (full problem context and dead ends)
- ~/claude/multi-agent/claude-023-postmortem (insights from prior attempt)

## The Problem

Prove: among any 2*alpha(r)+2 nonzero non-proportional vectors in F_p^{r+1} (p >= 5), there exist coefficients s_i in {1,...,p-1} supported on some subset with sum(s_i) <= p and sum(s_i * v_i) = 0.

Here alpha(3) = 8, so for r=3: 18 vectors in F_p^4.

## What's proved
1. Base case eta(C_p^3) = 8(p-1)+1 (Lean-verified)
2. Translation trick: s(C_p^r) = eta(C_p^r) + p - 1
3. Lower bound: eta(C_p^r) >= (2*alpha(r-1)+1)(p-1)+1 via doubled+e1
4. Two-fiber bound: if all vectors in <= 2 hyperplane fibers, done
5. Rank-3 theorem: non-degenerate collinear triples yield weight < p

## Dead ends (DO NOT attempt these)
- Character theory for support >= 4 (W(chi)=0 for even characters)
- k=4 parity theorem (WRONG)
- Cross-fiber collinear triple universality (0/94 failures have them)
- Classical CW fires only for p=5

## Your approach

Try the following proof strategy:

Assume for contradiction: 18 nonzero non-proportional vectors in F_p^4 with NO zero-sum of weight <= p.

Step 1: Choose a linear form w. Get fibers F_0, F_1, ..., F_{p-1}. By two-fiber bound, must have >= 3 nonempty fibers. By fiber induction, each fiber has <= 8 vectors.

Step 2: Consider the "copies pool" multiset: each vector v_i appears p-1 times. Total size = 17(p-1). A zero-sum of weight <= p in the original equals a subsequence of length <= p summing to zero in the copies pool.

Step 3: The Davenport constant D(C_p^4) = 4(p-1)+1. So the copies pool (size 17(p-1)) contains MANY zero-sum subsequences. The question is whether any has length <= p.

Step 4: Apply Grynkiewicz's Theorem 1.7 (the key tool for s_{kq}). With G = C_p^4, q = p, d = ceil(D*(G)/q) = ceil((4p-3)/p) = 4 (for p >= 5). Then:

For k > d(d-1)/2 = 6: s_{kp}(G) <= kp + D*(G) - 1.

So s_{7p}(C_p^4) <= 7p + 4p - 4 = 11p - 4. Our sequence has length 17(p-1) = 17p - 17.

For p >= 5: 17p - 17 >= 11p - 4 iff 6p >= 13, which holds for p >= 3.

So the copies pool has a zero-sum subsequence of length 7p! That's a zero-sum of weight 7p in the original. But we need weight <= p, not 7p.

Step 5: Can we improve? Theorem 1.7 with different X sets. Try X = {1, 2, ..., d} union {k}. For our problem: we want zero-sums of length p (weight p), 2p (weight 2p), etc. We need the one with length p.

Step 6: Apply Proposition 3.3. With d = 4 and p >= 5, k >= d: s_{kp}(G) <= kp + D*(G) - 1 for k >= 4. So s_{4p}(C_p^4) <= 4p + 4p - 4 = 8p - 4. Is 17(p-1) >= 8p - 4? That's 17p - 17 >= 8p - 4, so 9p >= 13, true for p >= 2.

So there EXISTS a zero-sum subsequence of length 4p. Weight 4p in the original. Still too large.

Step 7: What about using the stronger bound from Theorem 1.8? It requires d <= 4 AND p >= 2d-1 = 7. For p >= 7:

s_{kp}(C_p^4) <= kp + D*(G) - 1 for every k >= d = 4.

In particular, s_{p}(C_p^4) <= p + 4p - 4 = 5p - 4 for p >= 7.

Is 17(p-1) >= 5p - 4? That's 17p - 17 >= 5p - 4, so 12p >= 13. YES for p >= 2.

WAIT. Does Theorem 1.8 say k >= d, meaning k >= 4? Then s_{4p} <= 4p + D* - 1. But does it say s_p <= p + D* - 1? That would require k = 1 >= d = 4, which is FALSE.

READ THEOREM 1.8 CAREFULLY. It says: for k >= d and p >= 2d-1, s_{kp}(G) <= kp + D*(G) - 1. We need k >= 4. So we get s_{4p} <= 8p - 4 but NOT s_p.

Step 8: The gap is between k=1 (what we need) and k=4 (what the theorem gives). Can we bridge this gap using the STRUCTURE of our specific sequence?

The idea: our copies pool has a zero-sum of length 4p (from step 6). This is a weighted zero-sum with weight 4p. Can we DECOMPOSE it into smaller pieces? If the weight-4p zero-sum uses vectors from multiple fibers, perhaps one fiber's contribution has weight <= p.

Step 9: Explore this decomposition idea carefully. If sum(s_i * v_i) = 0 with sum(s_i) = 4p, and we partition by fiber: sum_{c} sum_{v in F_c} s_v * v = 0. For each fiber c, the contribution sum_{v in F_c} s_v * v is a vector in F_p^4 with first coordinate c * sum_{v in F_c} s_v. The first coordinates must sum to 0 mod p: sum_c c * W_c = 0 mod p, where W_c = sum_{v in F_c} s_v.

Can we choose the decomposition so that some W_c <= p?

Do this analysis carefully. Write Python code to verify on examples.

Save ALL findings (proved lemmas, dead ends, partial results) to ~/claude/grail-tasks/results-proof-attempt.txt
