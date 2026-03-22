# Inverse Theorem for η-Extremal Configurations: Seed Document

## What is known (PROVEN, do not re-derive)

### The η-constant
For a finite abelian group G with exponent exp(G), η(G) is the smallest integer l such that every sequence of l elements in G contains a zero-sum subsequence of length at most exp(G).

For elementary p-groups C_p^r: exp = p, so we seek zero-sums of length 1 to p.

### Exact value at rank 3
**Theorem (Fischer, 2026, Lean-verified).** η(C_p^3) = 8(p-1)+1 for all odd primes p.

The extremal construction A_8 consists of 8 nonzero vectors in F_p^3:
a_0=(1,0,0), a_1=(0,1,0), a_2=(0,0,1), a_3=(-1,1,1),
a_4=(1,1,0), a_5=(1,0,1), a_6=(-1,2,1), a_7=(-1,1,2).

### All-ranks lower bound
**Theorem (Fischer, 2026).** η(C_p^r) ≥ (9·2^{r-3} - 1)(p-1) + 1 for all r ≥ 3, all odd primes p.

Proof uses two ingredients:
1. **Doubling lemma.** If A ⊂ F_p^r is zero-sum-free (mult p-1, lengths ≤ p), then {(0,v),(1,v) : v in A} ⊂ F_p^{r+1} is also zero-sum-free.
2. **e_1 trick.** The vector e_1 = (1,0,...,0) can always be added to the doubled construction. Proof: any short zero-sum involving e_1 forces t_0 + Σs_i = p (first coordinate), then Σt_i = 0, and the remaining coordinates give a zero-sum in A of length < p. Contradiction.

Recurrence: α(r+1) ≥ 2α(r) + 1, with α(3) = 8. Solution: α(r) ≥ 9·2^{r-3} - 1.

### Computed values
- α(3,p) = 8 for all odd primes p (exact, both bounds proved)
- α(4,3) = 17 (exact, computed: no 18th vector exists in F_3^4)
- α(4,p) ≥ 17 for all odd primes (construction works for all p)
- α(4,p) ≤ 17 is OPEN for p ≥ 5

### Structure of the extremal set at r=4, p=3
The 17-vector construction in F_3^4 is:
- Layer 0: {(0,v) : v in A_8} = 8 vectors with first coordinate 0
- Layer 1: {(1,v) : v in A_8} = 8 vectors with first coordinate 1
- Extra: e_1 = (1,0,0,0)

Computationally verified: this is the UNIQUE maximal configuration up to the choice of which element from each {v,-v} pair to include (for e_1, both (1,0,0,0) and (2,0,0,0) work, but not both).

## What failed (DEAD ENDS, do not retry)

1. **Fourier/character-sum approach for rank ≥ 4.** The involution f_r(λ)+f_r(-λ) = rp pins the level function only at r=3 (because 3 is odd, k must equal 1 everywhere). For r=4, k(λ)+k(-λ)=3 allows k in {1,2}, creating 2^{(p-1)/2} possible half-sets. The Fourier constraints are underdetermined. Computed: 276 Fourier-compatible pairs at p=7, ALL survive ground truth. The method is completely toothless.

2. **Polynomial method (slice rank, partition rank, CLP).** All known bounds operate in the regime n→∞, fixed p. For fixed rank and varying p they give bounds like O(p^5) when the answer is 17. Wrong regime entirely.

3. **Projection-based character sums.** I computed Q(χ) using coordinate projections and found apparent "integrality violations." Sanity check showed the computation was wrong: projections of vectors ≠ kernel parametrization. False alarm.

## The goal: inverse theorem

### What we want to prove
**Conjecture (Inverse Theorem).** Let A be a maximal zero-sum-free set in F_p^r (at multiplicity p-1, lengths ≤ p). Then there exists a coordinate projection π: F_p^r → F_p and a maximal zero-sum-free set B in ker(π) ≅ F_p^{r-1} such that:

A = {v in F_p^r : π(v) = 0, v' in B} ∪ {v in F_p^r : π(v) = 1, v' in B} ∪ {e_π}

where v' is the projection of v onto ker(π) and e_π is the unit vector in the π direction.

In other words: every maximal configuration is a doubled-plus-e_1 of a maximal configuration in one lower dimension.

### Why this would suffice for the upper bound
If the inverse theorem holds, then α(r) = 2α(r-1) + 1 EXACTLY, giving α(r) = 9·2^{r-3} - 1 and η(C_p^r) = (9·2^{r-3} - 1)(p-1) + 1 for all r ≥ 3.

### Precedent
Inverse theorems exist for zero-sum-free sequences near the Davenport constant length (Gao-Geroldinger Theorem 4.8): extremal sequences in C_p^r of length D(C_p^r) must have very specific structure (support is an independent set). The analogous question for η-extremal sequences is unstudied.

### Possible approaches

**Approach A: Fiber analysis.**
Project A onto one coordinate. The fibers A_c = {v in A : π(v) = c} for c in F_p partition A. If |A| = 9·2^{r-3} - 1, analyze how the elements distribute across fibers. If most elements concentrate in two fibers (c=0 and c=1), the structure forces a doubled construction.

**Approach B: Forbidden subconfigurations.**
A maximal set A cannot contain certain local patterns (e.g., three vectors summing to zero, or p vectors with the right multiplicity structure). Classify which patterns are forbidden and show that avoiding all of them forces the product structure.

**Approach C: Start with r=4, p=3.**
The problem is fully concrete: F_3^4 has 80 nonzero vectors. A zero-sum-free set (at mult 2, lengths ≤ 3) has size exactly 17. We computed that the unique maximal set is the doubled-plus-e_1 of A_8. Can we prove this WITHOUT exhaustive enumeration? Understanding WHY the structure must be this way for p=3 might reveal the general argument.

**Approach D: Eigenvalue/spectral methods.**
Define a graph on F_p^r \ {0} where edges connect vectors whose sum or triple-sum creates a zero-sum. The zero-sum-free sets are independent sets of this graph. The Lovász theta function or spectral gap might give structural information about maximum independent sets.

## Key quantities
- p = prime (start with p=3,5,7)
- r = rank (start with r=4)
- α(r,p) = max |A| for A zero-sum-free in F_p^r at multiplicity p-1
- For p=3: zero-sum-free means no antipodal pair and no 3-element zero-sum (this is a cap set condition + halving)
- For general p: the condition involves ALL weighted sums Σ t_i v_i = 0 with 0 ≤ t_i ≤ p-1 and 1 ≤ Σt_i ≤ p

## Computational tools available
The worker has a `compute` tool for sandboxed Python. Can enumerate vectors, check zero-sum conditions, classify configurations, compute graph spectra. Use it freely for r=4 at small primes.

## What counts as real progress
- Proving the inverse theorem for r=4, p=3 (even a non-enumerative proof)
- Proving any structural constraint on maximal configurations (e.g., "the fiber distribution must be (n, n, 1, 0, ..., 0)")
- Identifying a graph-theoretic or algebraic invariant that distinguishes the doubled-plus-e_1 structure from all other candidates
- Reducing the general inverse theorem to a simpler statement that can be checked computationally
