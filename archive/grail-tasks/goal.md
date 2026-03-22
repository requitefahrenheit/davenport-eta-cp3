# THE GRAIL: All-Ranks Upper Bound

## The Exact Target Theorem

**Weight Flexibility Theorem.** For all r ≥ 3 and all odd primes p: given α(r)+1 = 9·2^{r−3} non-proportional nonzero vectors in F_p^r, each with multiplicity p−1, the set of achievable zero-sum weights W ⊆ {1,...,p} satisfies |W| ≥ (p+1)/2.

This is the SINGLE theorem that implies the Grail (η(C_p^r) = (9·2^{r−3}−1)(p−1)+1 for all r ≥ 3).

## Why This Implies the Grail

Given 2α+2 = 9·2^{r−2} vectors in F_p^r:
1. Project via π: F_p^r → F_p. Get fibers.
2. If fiber 0 has ≥ α+1 vectors: zero-sum by induction. Done.
3. Otherwise: ≥ α+2 vectors in nonzero fibers, spanning ≥ 2 fibers.
4. Two nonzero fibers c₁, c₂ each with ≥ α+1 vectors (or redistribute).
5. Weight Flexibility: each fiber has |W_i| ≥ (p+1)/2 achievable zero-sum weights.
6. Cauchy-Davenport: |c₁·W₁ + c₂·W₂| ≥ min(p, |W₁|+|W₂|−1) = p.
7. So ∃ w₁ ∈ W₁, w₂ ∈ W₂ with w₁c₁+w₂c₂ ≡ 0 mod p.
8. Combined weight w₁+w₂ ≤ 2p. If > p, take complements (p-w₁ from fiber c₁).
9. ∴ zero-sum of weight ≤ p in F_p^r. ∎

## What's Already Proved

- Base case: At rank 3, the Shadow Window Theorem shows |W| ≥ (p−1)/2 for A₈ specifically. Need to show this for ALL sets of 9 vectors, and at all ranks.
- The analogous lower bound |W| ≥ 1 is the definition of η.

## Approaches (PURE THEORY ONLY)

### Approach 1: Inductive Weight Flexibility
Assume Weight Flexibility at rank r−1. Derive it at rank r. The zero-sums at rank r are built from zero-sums at rank r−1 in fibers. If a fiber's projected vectors have weight set W', the lifted zero-sums have the SAME weight set. So the inductive hypothesis propagates directly to fibers. The question: does combining fibers preserve weight flexibility?

### Approach 2: Polytope Dimension Argument
The zero-sum coefficients live in a polytope P ⊆ [0,p−1]^m defined by r linear equations (Σc_i v_{ij} = 0). Dimension ≥ m−r. The weight functional w(•) = Σc_i restricted to P has range [w_min, w_max]. For m−r ≥ p, the range should cover at least (p+1)/2 integer values. Can we bound the range of a linear functional on a lattice polytope?

### Approach 3: Perturbation / Exchange Argument
Given a zero-sum at weight w, perturb: increase c_j by 1 (weight +1), compensate by solving Σδ_i v_i = -v_j with Σδ_i = 0 in the remaining m−1 coefficients. This is r+1 equations in m−1 unknowns. For m >> r, solutions exist within the box [0,p−1]. Each perturbation shifts weight by 1. So W contains an interval around w.

### Approach 4: Character Sum / Generating Function
The generating function F(t) = Σ_{w=1}^{p} |{zero-sums of weight w}| · t^w encodes the weight distribution. If we can show F has ≥ (p+1)/2 nonzero coefficients using character sum estimates, we'd be done. The rank-3 Fourier argument might generalize.

### Approach 5: Reduction to Davenport Constant
The Davenport constant D(G) controls zero-sum-free sequences without weight restrictions. Known: D(C_p^r) = r(p−1)+1. Connection to η: for the weight-restricted problem, having extra vectors (beyond what D requires) should give weight flexibility. With α+1 >> r vectors, we have massive surplus over D.

## Rules

1. NO COMPUTATION. Proofs and reductions only.
2. Push each approach to a NAMED OBSTRUCTION.
3. The polytope dimension argument (Approach 2) seems most elementary.
4. The perturbation argument (Approach 3) seems most concrete.
5. Remember: |W| ≥ (p+1)/2 is the target. Even |W| ≥ 2 would be progress.
