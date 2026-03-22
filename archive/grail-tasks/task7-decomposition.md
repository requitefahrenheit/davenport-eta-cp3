# Task: Zero-Sum Decomposition Strategy

Read ~/claude/multi-agent/seeds/grail-briefing.md for context.

## The Core Idea

We KNOW a zero-sum of weight 4p exists (from the Davenport constant bound on the copies pool). We need weight <= p. Can we decompose the weight-4p zero-sum into smaller pieces?

## Setup

Let S be 17 nonzero non-proportional vectors in F_p^4, each with multiplicity p-1. The copies pool |S| = 17(p-1).

D(C_p^4) = 4(p-1)+1. So any subsequence of length 4(p-1)+1 contains a zero-sum.

Our pool has length 17(p-1) = 4 * (4(p-1)+1) + (p-5). So we can find AT LEAST 4 disjoint zero-sum subsequences (for p >= 5).

Claim: among these 4+ disjoint zero-sums, at least one has length <= p.

## Why this might work

If T1, T2, T3, T4 are disjoint zero-sum subsequences, their total length is >= 4. But also <= 17(p-1). The AVERAGE length is <= 17(p-1)/4.

For the average to exceed p, we'd need 17(p-1)/4 > p, i.e., 17p-17 > 4p, i.e., 13p > 17. True for p >= 2. So the average is ~4p, not useful.

But: each T_i has length divisible by p (it's a zero-sum in C_p^4, so length is divisible by exp(G) = p? NO! Zero-sums can have any length >= 1 in general.)

Actually, for the EGZ constant: zero-sum subsequences of length EXACTLY p are what we want. The constant s_p(G) counts when these are guaranteed. We know s_p(C_p^4) >= 17(p-1)+1 (that's what we're trying to prove as an UPPER bound). So this is circular.

## Better approach: Disjoint short zero-sums via Theorem 1.7

Grynkiewicz's Theorem 1.7 with X = {1, 2, 3, 4} (looking for zero-sums of length p, 2p, 3p, or 4p):

With d = 4, X = {1,2,3,4}: [1,max X] \ X = empty set. Condition (1) is vacuous (empty product = 1 != 0 mod p).

So s_{X*p}(G) <= (4 - 4 + 1)p + D*(G) - 1 = p + 4p - 4 = 5p - 4.

Our pool has 17(p-1) >= 5p-4 for p >= 2. So: there exists a zero-sum of length kp for some k in {1,2,3,4}.

If k=1: we're done! Weight p. But k could be 2, 3, or 4.

## The Alon-Dubiner trick

Reiher's Kemnitz proof uses this: if you have a zero-sum of length 3p, remove any element g, and the remaining length-(3p-1) subsequence has N_{2p}(T \ g) >= 1 (by another CW argument). So there's a zero-sum of length 2p INSIDE the 3p one. The complement is a zero-sum of length p.

## Your task

Write Python code to:

1. At p=5: take the doubled+e1 construction (17 vectors, each with mult 4, pool size 68). Find a zero-sum of length 20 (=4p). Then try to decompose it: is there a subset of length 5 (=p) that's also a zero-sum?

2. More systematically: given a zero-sum of length kp (k >= 2), when can we find a zero-sum of length p inside it? This is related to N_p(T) > 0 for the subsequence T.

3. Apply the Reiher/Alon-Dubiner cascading argument: if a length-3p zero-sum T exists, and for every g in T we have N_{2p}(T \ g) > 0, then T contains a length-p zero-sum (complement of the 2p one). Verify this computationally.

4. Set up the CW congruences for the SUBSEQUENCE (not the full pool). If T has length 3p, with specific vectors, do the CW congruences force N_p(T) > 0?

5. Can we prove: for ANY zero-sum of length kp (k <= 4) in C_p^4, there exists a zero-sum of length p inside it? This would close the grail immediately.

Save results to ~/claude/grail-tasks/results-decomposition.txt
