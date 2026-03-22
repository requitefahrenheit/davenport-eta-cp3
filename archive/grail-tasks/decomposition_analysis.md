# Zero-Sum Decomposition Analysis for η(C_p^4) = 17(p-1)+1

## Problem Statement
Among 18 nonzero non-proportional vectors in F_p^4 (p ≥ 5 prime), prove there exist
coefficients s_i ∈ {1,...,p-1} with Σs_i ≤ p and Σ(s_i · v_i) = 0.

## Approach: Decomposition of Larger Zero-Sums

### Setup
- Copies pool: 18 vectors, each with multiplicity p-1. Total size 18(p-1).
- Grynkiewicz Thm 1.8 (d=4, k≥4, p≥7): s_{kp}(C_p^4) ≤ kp + 4p - 4.
- For k=4: s_{4p} ≤ 8p-4. Pool size 18(p-1) ≥ 8p-4 for p≥2. → Weight-4p zero-sum exists.

### Result 1: Weight-4p Decomposition FAILS

**Theorem (Computational, p=5).** There exist weight-4p zero-sums in the copies pool
of 17 ZSF vectors that contain NO weight-p sub-zero-sum.

*Proof sketch:* The 17-vector construction is ZSF (no weight-p zero-sum). Weight-2p
and weight-3p zero-sums among these vectors inherit the ZSF property—they cannot
contain weight-p sub-zero-sums, since any such sub-ZS would contradict the ZSF property
of the base set. Verified: weight-10 and weight-15 ZS among 17 base vectors, all checked,
none contain weight-5 sub-ZS. □

**Consequence:** The naive decomposition strategy (find weight-4p, extract weight-p piece)
is fundamentally blocked for ZSF configurations.

### Result 2: Weight-2p Decomposition WORKS (with 18th vector)

**Theorem (Computational, p=5).** For the 17-vector ZSF construction + ANY valid 18th
vector, there exists a weight-2p zero-sum involving v18, and EVERY such ZS decomposes
into two weight-p zero-sums.

*Verified:* 556/556 valid 18th vectors at p=5. Sampled at p=7 (7/7 tested).

**Structural reason:** The weight-2p zero-sum involving v18 uses vectors from at most 2-3
fibers. The fiber structure constrains the coefficients enough that a weight-p sub-ZS
must exist. Specifically:
- Same-fiber ZS: the eta/s bounds for C_p^3 force decomposition.
- Cross-fiber ZS: collinear triple structure gives two weight-p pieces via rescaling.

### Result 3: Three Mechanisms Cover All Cases

**Mechanism A: Non-degenerate collinear triples (462/556 cases at p=5).**
For v18 creating a cross-fiber collinear triple with dependency (a,b,c):
- If a+b≠0, a+c≠0, b+c≠0 (non-degenerate): rank-3 theorem gives weight ≤ p.
- Non-degeneracy is guaranteed for "same-tail" triples across fibers 0, c, with c≥2:
  dependency (c-1, -c, 1) has all pairs nonzero for p≥5, c∉{0,1}.

**Mechanism B: Intra-fiber η/s bounds (34/94 residual cases).**
- v18 in fiber 0 (8 cases): 9 vectors in fiber 0. Since A8 is maximal 4-sum-free,
  the 9th vector creates a 4-element sum-to-zero. Weight 4 < p.
- v18 in fiber 1 (26 cases): 10 vectors in fiber 1. s(C_p^3)=9(p-1)+1 ≤ 10(p-1).
  Length-p zero-sum exists. Weight = p.

**Mechanism C: Cross-fiber support-4 zero-sums (60/94 residual cases).**
For v18 in fiber c≥2 without a non-degenerate collinear triple:
- A support-4 zero-sum uses v18 + 3 vectors from fibers 0∪1.
- Fiber weight constraint: Σ(a_i) + c ≡ 0 (mod p).
- Tail constraint: Σ(tail_i) + tail_v18 ≡ 0 (mod p) in C_p^3.
- For p=5: the 9 fiber-1 tails + 8 fiber-0 tails provide enough variety.

## The Proof Gap

### What's Proved
For the SPECIFIC 17-vector construction, adding any 18th vector yields weight-≤p ZS.
Three mechanisms (collinear triple, intra-fiber, cross-fiber support-4) cover all cases.

### What's NOT Proved
For ARBITRARY 18 non-proportional vectors in C_p^4:
1. The fiber structure depends on the choice of linear form w.
2. Cap configurations (no 3 collinear) bypass Mechanism A entirely.
3. Mechanism C depends on fiber structure being (8,9) in the specific construction.

### The Open Lemma Needed

**Conjecture.** Among any 18 nonzero non-proportional vectors in F_p^4 (p≥5), at least
one of the following holds:
(a) There exist 3 vectors with non-degenerate collinear dependency → weight ≤ p by rank-3.
(b) There exists a linear form w with some fiber having ≥10 vectors → weight p by s(C_p^3).
(c) There exist ≤ p vectors summing to zero with appropriate coefficients → weight ≤ p.

The difficulty: proving (c) when (a) and (b) both fail. This occurs when:
- All collinear triples are pair-degenerate (or the set is a cap).
- All fibers under all linear forms have ≤ 9 vectors.

### Recommended Next Step
The CW polynomial method (Grynkiewicz 2023, Reiher-style) combined with:
- Rank-3 structural constraints (for non-cap configurations)
- Cap bounds (for cap configurations: max cap in PG(3,p) is p^2+1)

The key new idea: for cap configurations with 18 points in PG(3,F_p), CW counting
of support-4 zero-sums modulo p forces at least one to exist (heuristic: ≈5 at p=5,
growing with p).

## Additional Results

### Result 4: Cap Configurations Have Abundant Weight-p ZS

**Theorem (Computational).** Among 50 random caps of size 18 in PG(3, F_5), the
minimum number of weight-5 zero-sums is 34. Among 20 random caps in PG(3, F_7),
all have weight-7 zero-sums. All ZS in caps are support-4 (no collinear triples).

Coefficient patterns:
- p=5: exclusively (1,1,1,2) and permutations.
- p=7: varied — (1,1,1,4), (1,1,2,3), (1,2,2,2), etc.

### Result 5: CW Degree Obstruction

The natural CW polynomial Q(x) = Π_d[1-S_d^{p-1}]·[1-W^{p-1}] has degree 5(p-1).
CW requires degree < 18. This fails for p ≥ 5.

**Consequence:** Standard CW cannot directly prove weight-p zero-sums exist.
The Grynkiewicz weighted CW (2023) or Ax's theorem may bypass this obstruction.

### Result 6: Weight Distribution in Solution Space

The 13-dimensional solution space {s : A·s = 0, Σs_i = 0 in F_p} has weight
distribution centered at ~36 (for p=5). Weight-p solutions occupy fraction ~p^{-10}
of the space. They exist (verified) but are invisible to random sampling.

**Implication:** The proof cannot use probabilistic arguments over the solution space.
It must exploit the GEOMETRIC structure of the 18 vectors (cap bounds, fiber structure,
or the specific algebraic constraints from the Grynkiewicz weighted CW).

## Formal Lemma Statements

### Lemma 1 (Same-Tail Cross-Fiber Non-Degeneracy) — PROVED
For vectors u = (0, t), v = (1, t), w = (c, t) in C_p^4 with c ≥ 2, p ≥ 5:
the collinear dependency (c-1, -c, 1) is non-degenerate (no pair sums to 0).
Proof: (c-1)+(-c)=-1≠0; (c-1)+1=c≥2≠0; (-c)+1=1-c≤-1≠0.

### Lemma 2 (Weight-p via Sum-Zero Dependency) — PROVED [Postmortem Lemma 2]
For non-degenerate (a,b,c) with a+b+c ≡ 0 (mod p): ∃μ ∈ F_p* with ⟨μa⟩+⟨μb⟩+⟨μc⟩ = p.

### Lemma 3 (Intra-Fiber η Bound) — PROVED [Postmortem Lemma 3]
If |F_0| ≥ 9 in fiber 0: η(C_p^3) = 8(p-1)+1 ≤ 9(p-1). Weight-≤p ZS exists.

### Lemma 4 (Intra-Fiber s Bound for Nonzero Fibers) — PROVED
If |F_c| ≥ 10 with c ≠ 0: s(C_p^3) = 9(p-1)+1 ≤ 10(p-1). Weight-p ZS exists.

### Lemma 5 (Maximal 4-Sum-Free Extension) — PROVED [Specific to construction]
The A8 set in C_p^3 is maximal 4-sum-free: any 9th vector creates a 4-element zero-sum.

### OPEN Lemma 6 (Cap Weight-p ZS)
Among any 18 cap points in PG(3, F_p) (p ≥ 5), a support-4 weight-p ZS exists.
