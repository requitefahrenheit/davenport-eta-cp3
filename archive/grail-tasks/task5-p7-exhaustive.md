# Task: Exhaustive Verification at p=7

Read ~/claude/multi-agent/seeds/grail-briefing.md for context.

## Background

At p=5, we verified: among ANY 18 nonzero non-proportional vectors in F_5^4, there exists a zero-sum of weight <= 5. The verification checked all 607 possible 18th vectors extending a specific 17-vector construction, with zero failures.

We need the same verification at p=7. The construction at p=7:

A8 = {e1, e2, e3, -e1+e2+e3, e1+e2, e1+e3, -e1+2e2+e3, -e1+e2+2e3} in F_7^3.

The doubled+e1 construction in F_7^4:
Fiber 0: (0, a2, a3, a4) for each (a2,a3,a4) in A8 -- 8 vectors
Fiber 1: (1, a2, a3, a4) for each (a2,a3,a4) in A8, plus (1,0,0,0) -- 9 vectors
Total: 17 vectors.

For p=7: there are 7^4 - 1 = 2400 nonzero vectors. After removing proportional copies (dividing by p-1=6): 2400/6 = 400 projective classes. Minus the 17 already used: 383 candidate 18th vectors.

## Your computation

Write a Python script that:

1. For EACH of the 383 candidate 18th vectors v18:
   a. Form the 18-vector set S = {v1,...,v17, v18}
   b. Search for a zero-sum: coefficients s_i in {1,...,6} with sum(s_i) <= 7 and sum(s_i * v_i) = 0 (in F_7^4)
   c. Search strategy: first check support-3 (collinear triples with non-degenerate or triplesum-zero dependency). Then check support-4 (four vectors summing to zero). Then support-5 if needed.
   d. Record: which mechanism kills it, what the zero-sum is.

2. Classification: group the 383 candidates by:
   - Fiber of v18 (first coordinate 0,1,2,...,6)
   - Mechanism that kills it (support-3 nondeg, support-3 triplesum0, support-4, support-5, other)
   - Whether a cross-fiber collinear triple exists

3. Report any FAILURES (candidates where no weight-<=7 zero-sum is found). These would be counterexamples to the grail conjecture.

4. Compare with p=5 results: is the pattern similar? Do the same mechanisms dominate?

IMPORTANT: This computation may be slow. The support-3 check requires iterating over C(18,3) = 816 triples and for each, checking rank and dependencies. Support-4 requires C(18,4) = 3060 quadruples. Optimize:
- For support-3: build the 4x18 matrix, compute kernel. Iterate over kernel vectors with support <= 3.
- For support-4: check all 4-element subsets summing to zero in F_7^4 first (just addition, no scaling needed -- weight = 4 < 7 = p).

Target: complete in under 30 minutes. If it takes longer, do p=7 only for fiber-0 candidates first (about 50 candidates).

Save results to ~/claude/grail-tasks/results-p7-exhaustive.txt
