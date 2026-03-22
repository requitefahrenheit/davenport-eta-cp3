# Computational Findings — Round 1 (Computer Agent)
## Shadow Saturation for ZSF Sets

### FINDING 1: Shadow Saturation Verified
Shadow of the 17-vector doubled+e₁ construction covers ALL nonzero vectors in F_p^4 at weight p-1:
- p=5: 624/624 ✓
- p=7: 2400/2400 ✓
- p=11: 14640/14640 ✓
- p=13: 28560/28560 ✓

### FINDING 2: N(v) mod p is NOT Uniform
The representation count N(v) = #{coefficient tuples reaching v at weight ≤ p-1} is NOT constant mod p.
At p=5: N(v) mod 5 takes ALL values {0,1,2,3,4}. Distribution: {0:99, 1:162, 2:131, 3:113, 4:119}.
At p=7: Same, all 7 residues appear.
**Implication: A simple CW congruence N(v) ≡ c ≠ 0 (mod p) CANNOT prove saturation.**

### FINDING 3: CW Degree Fires Only at p=5
The Chevalley-Warning degree condition 4(p-1) < 17 holds iff p=5.
- p=5: 4(4) = 16 < 17, slack 1. CW fires.
- p=7: 4(6) = 24 > 17. CW does NOT fire.
**Implication: CW polynomial method is a DEAD END for p ≥ 7.**

### FINDING 4: Fiber Structure Completely Characterized
For the standard construction with linear form w = first coordinate:
- **Fiber (p-1)**: ALL p³ targets need weight exactly p-1. Zero budget for fiber-0 vectors.
- **Fibers 0 through p-2**: Each has exactly gap(A8, p-2) last-weight targets.
  - p=5: 38 each
  - p=7: 50 each
  - p=11: 74 each
  - p=13: 86 each
- **Verified at all tested primes.**
- **Formula**: gap(A8, p-2) = (p³-1) - |shadow_{p-2}(A8)| where A8 is the rank-3 extremal set.

### FINDING 5: Fiber-(p-1) Saturation = Rank-3 Theorem
The 9 fiber-1 vectors project to A8 ∪ {0} in F_p³.
- The zero projection (from e₁) contributes nothing.
- The 8 nonzero projections ARE A8 (the rank-3 extremal set).
- A8 shadow at weight p-1 covers ALL of F_p³ — this IS the proved η(C_p³) theorem.
- **So fiber-(p-1) saturation follows from the base case.**

### FINDING 6: A8 Shadow Growth Formula
**g(w) = 6w² + 2 is EXACT for w ≤ ⌊(p-1)/2⌋.**
First deviation always = -4 at w = ⌊(p-1)/2⌋ + 1.
Verified at p = 5, 7, 11, 13, 17, 19, 23.

Growth data (stabilized for large p):
- wt 1: 8
- wt 2: 26
- wt 3: 56
- wt 4: 98
- wt 5: 152
- wt 6: 218
- wt 7: 296
- wt 8: 386
- wt 9: 488
- wt 10: 602
- wt 11: 728

The quadratic growth alone gives cumulative ≈ 2(p-1)³/3, only ~2/3 of the needed p³-1.
Growth at weights > (p-1)/2 peaks and then decreases as the shadow approaches saturation.

### FINDING 7: Uniqueness of Standard Construction
Random greedy ZSF search: 0/30 attempts at p=7 found ANY eta-ZSF 17-set.
Confirms prior finding: doubled+e₁ is apparently the unique eta-ZSF 17-set at p=5 and p=7.

### FINDING 8: ZSF Shadow is SMALLER at Low Weights
At p=5, weight ≤ 2: ZSF construction covers 104 targets vs median 132 for random 17-point sets.
ZSF ranked LAST (0th percentile) among 50 random sets.
**The ZSF condition restricts the shadow, not expands it.**

### FINDING 9: Hardest Targets
44 targets at p=5 have exactly N=1 representation (barely reachable).
These include:
- (k, 0, 0, 0) for k=1,2,3,4: only reachable as k·e₁
- (k, 1, 4, 3) and (k, 1, 3, 4) for k=1,...,4: require specific coefficient patterns
All hardest targets need support ≤ 3 (at most 3 vectors used).

### FINDING 10: Weight-2 Shadow Size
|shadow_2| = |{2v_i}| ∪ |{v_i + v_j}| = 17 + 82 = 99 (independent of p).
The 5 additional cumulative targets (104 - 99 = 5) come from weight-1 vectors not already counted.
Actually shadow_2 cumulative = shadow_1 ∪ shadow_2 = 17 + 87 = 104.

### FINDING 11: Subgroup Structure
The shadow at NO weight level forms an additive subgroup of F_p^4 (checked at p=5).
Not negation-closed at any weight either.

### KEY IMPLICATIONS FOR PROOF STRATEGY

1. **CW is dead for p ≥ 7.** Don't pursue polynomial method.
2. **Fiber decomposition is the right framework.** The hardest case (fiber p-1) already follows from the proved base case.
3. **The 6w²+2 growth formula for A8** could be provable combinatorially and might lead to quantitative shadow bounds.
4. **Sumset growth approach**: The growth data is structured but NOT governed by a single clean formula. The growth accelerates beyond 6w²+2 at high weights.
5. **The ZSF property makes shadows SMALLER, not larger.** Any shadow saturation proof must use the ZSF condition in a non-obvious way — perhaps through the rank-3 theorem as a black box.
