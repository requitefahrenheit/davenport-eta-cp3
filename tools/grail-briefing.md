# The Grail: η(C_p^{r+1}) = (2α(r)+1)(p−1)+1 for all r ≥ 3, all p ≥ 5

## The Problem in Plain Language

Given 2α(r)+2 nonzero vectors in F_p^{r+1} (no two proportional), prove there exist
coefficients s_1, ..., s_k ∈ {1, ..., p-1} (not all zero) with s_1*v_1 + ... + s_k*v_k = 0
and s_1 + ... + s_k ≤ p.

Here α(r) = 9·2^{r-3} - 1 for r ≥ 3 (so α(3) = 8, α(4) = 17, α(5) = 35).

The base case r = 3 is PROVED (Lean-verified). The inductive step is open.

## What Is Proved

1. **η(C_p³) = 8(p−1)+1** for all p ≥ 5. Lean-verified. Two independent proofs (lower bound via explicit construction, upper bound via generating functions + characters).

2. **s(C_p^r) = η(C_p^r) + p − 1** for all r ≥ 1, all p ≥ 3. "Translation trick." Proof: a length-p zero-sum uses coefficients summing to p; subtracting gives an (η-length) zero-sum of weight ≤ p. Five lines.

3. **η(C_p^r) ≥ (2α(r-1)+1)(p−1)+1** for all r ≥ 4. "Doubled+e₁" construction: take two copies of the rank-(r-1) extremal set on parallel hyperplanes, add e₁.

4. **Two-fiber upper bound.** If all vectors lie in at most 2 hyperplane fibers (w(v) ∈ {0, c} for some linear form w and constant c), then α(r+1) ≤ 2α(r)+1. Proved via the inductive η and s bounds.

5. **Proportionality lemma.** No ZSF set contains two proportional vectors.

## What Is Verified Computationally

- α(4, 5) = 17 = 2·8 + 1. All 607 possible 18th vectors tested. Zero failures.
  - 513/607 killed by support-3 (rank-3 subroutine)
  - 94/607 killed by support-4 (four vectors summing to zero, weight 4 < p)

## The Exact Gap

The two-fiber bound handles configurations with ≤ 2 nonempty fibers. The gap is: **multi-fiber configurations** (vectors spread across ≥ 3 hyperplane fibers).

When adding the 18th vector v₁₈ to the 17-vector construction, support-3 analysis (rank-3 subroutine) handles 513/607 cases. The 94 residual cases require support-4 zero-sums: four vectors summing to zero at weight 4 < p = 5.

## Dead Ends (DO NOT REVISIT)

### 1. Character theory for support ≥ 4: DEAD
The rank-3 upper bound proof pins f₃(μ) to a SINGLE level: f₃(μ) = p + ⟨μs⟩. This is specific to k = 3 summands. At k = 4: TWO possible levels exist.

### 2. The k=4 parity theorem: WRONG
**THE BUG:** W(χ) = 0 for ALL nontrivial even characters. The pairing μ ↔ (p−μ) gives μ·χ(μ⁻¹) + (p−μ)·χ(−μ⁻¹) = p·χ(μ⁻¹) when χ is even. Summing: 0. The Fourier extraction step divides by zero. 40 genuine non-degenerate support-4 ZSF tuples exist at p = 5.

### 3. Cross-fiber collinear triples: WRONG
The dependency (c−1, −c, 1) IS always non-degenerate for c ≥ 2. BUT 0/94 failures have such a cross-fiber collinear triple. The failures are killed by same-fiber 4-element zero-sums.

### 4. Combining pairwise-degenerate kernel vectors: DEAD

## Structural Findings

### Fiber anatomy of the 94 failures (p = 5)
- v₁₈ in fiber 0: 4-sum = (0,0,0,0). Four vectors from fiber 0.
- v₁₈ in fiber 2: 4-sum = (1,1,1,2). Three from fiber 1 + v₁₈.
- v₁₈ in fiber 3: 4-sum = (0,1,1,3). One from fiber 0 + two from fiber 1 + v₁₈.
- v₁₈ in fiber 4: 4-sum = (0,0,1,4). Two from fiber 0 + one from fiber 1 + v₁₈.
All first coordinates sum to 0 mod 5.

### A8 is maximal 4-sum-free
A8 has 8 elements in F₅³ with NO 4-element subset summing to zero. Adding any of 8 specific vectors creates a four-element zero-sum. A8 is MAXIMAL 4-sum-free.

### The rank-3 subroutine
For a collinear triple with dependency (−α, −β, 1): non-degenerate iff α ≠ 1, β ≠ 1, α+β ≠ 0.
At p = 5: 44% non-degenerate. At p = 13: 77%. As p → ∞: → 100%.
When non-degenerate, the rank-3 theorem guarantees weight < p.

## Promising Directions

### Direction 1: Polynomial Method (Chevalley-Warning)
Grynkiewicz (2023, Combinatorica 43(6)) generalizes CW with weights. Reiher proved Kemnitz (rank 2) this way: CW congruences gave 3 equations in 3 unknowns, inconsistent when N_p = 0.

For rank 4: CW gives ~13 congruences on N_j with ~16 unknowns. Underdetermined alone. BUT the rank-3 theorem adds structural constraints. Nobody has combined these tools.

Key reference: https://www.diambri.org/CWAK-015.pdf

### Direction 2: Induction on the number of fibers
Show multi-fiber ZSF always contains (a) a non-degenerate collinear triple, OR (b) a sub-configuration reducible to fewer fibers.

### Direction 3: ZSF constraint on fiber projections
The ZSF condition constrains fiber projections beyond point-set conditions. Perhaps it forces projections to be "large" in an additive sense, forcing 4-element zero-sums.

## The Construction

Fiber 0 (8 vectors): (0,1,0,0), (0,0,1,0), (0,0,0,1), (0,p-1,1,1), (0,1,1,0), (0,1,0,1), (0,p-1,2,1), (0,p-1,1,2)
Fiber 1 (9 vectors): (1,1,0,0), (1,0,1,0), (1,0,0,1), (1,p-1,1,1), (1,1,1,0), (1,1,0,1), (1,p-1,2,1), (1,p-1,1,2), (1,0,0,0)

## What Would Constitute a Proof

Show: for ANY 18 nonzero non-proportional vectors in F_p^4, there exist coefficients s_i ∈ {1,...,p-1} supported on some subset, with Σs_i ≤ p and Σs_i·v_i = 0.

The proof may assume (by the two-fiber bound) that vectors span ≥ 3 fibers.
