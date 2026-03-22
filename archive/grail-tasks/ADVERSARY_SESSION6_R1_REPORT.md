# ADVERSARY SESSION 6 ROUND 1 — ATTACK REPORT

## HEADLINE: FIVE GAPS FOUND. ONE IS CRITICAL. THE PROOF CHAIN IS NOT CLOSED.

---

## ATTACK 1: THE LIFT LEMMA HAS A GAP WITHOUT A ZERO-TAIL VECTOR (CRITICAL)

**Target:** The 8-tail bound — "any strongly ZSF 17-set has ≤ 8 projective tail lines."

**The proof strategy:** Project to tails → rank-3 theorem gives zero-sum of weight ≤ p → lift to F_p^4.

**The gap:** A 17-set with 9 tails can have NO zero-tail vector: 8 tails × mult 2 + 1 tail × mult 1 = 17. The lift argument relies on the e₁ vector to adjust the first coordinate. Without it, the argument breaks.

### Detailed Analysis

Given a rank-3 zero-sum Σ S_j t_j = 0 with W = ΣS_j ≤ p, the lift requires:

    Σ c_j^a · D_j ≡ -F  (mod p)

where D_j = a_j - b_j (fiber difference), F = Σ S_j b_j, and 0 ≤ c_j^a ≤ S_j.

**With e₁ present:** Add parameter c_e ∈ {0,...,p-W}. The achievable set V has |V| ≥ W+1 values, and c_e provides p-W+1 additional targets. By pigeonhole: (W+1) + (p-W+1) = p+2 > p. Intersection guaranteed. ✓

**Without e₁:** Need -F ∈ V directly. |V| ≥ min(p, W+1) by iterated Cauchy-Davenport. If W ≥ p-1: |V| = p, works. If W < p-1: |V| < p, target might be missed. ✗

### Why high-weight zero-sums aren't guaranteed

- s(C_p³) = 9p-8. We have 9(p-1) = 9p-9 < s(C_p³). Weight-p zero-sum NOT guaranteed.
- For p ≥ 11, 9 points can form an arc in PG(2,F_p) (no 3 collinear). Max arc = p+1 > 9 for p ≥ 11.
- On an arc: minimum zero-sum support = 4, minimum weight = 4.
- For a support-4 zero-sum at weight 4: |V| ≥ 5. For p = 17: 5 < 17. The 12 missing elements could include -F.

### Quantitative failure estimate

For support-m zero-sum with all S_j = 1: Π(S_j+1) = 2^m candidate tuples.

| p | Need 2^m ≥ p | Min support needed | Guaranteed? |
|---|---|---|---|
| 5 | 2³ = 8 ≥ 5 | 3 | ✓ (always have support ≥ 3) |
| 7 | 2³ = 8 ≥ 7 | 3 | ✓ |
| 11 | 2⁴ = 16 ≥ 11 | 4 | ✓ (4 vectors on arc → support 4) |
| 13 | 2⁴ = 16 ≥ 13 | 4 | ✓ |
| **17** | **2⁴ = 16 < 17** | **5** | **? (minimum support is 4, not 5)** |
| 19 | 2⁵ = 32 ≥ 19 | 5 | ? (need support-5 zero-sum) |

**At p = 17:** A support-4 zero-sum from an arc gives |V| ≤ 16 < 17. The lift can fail. This is the FIRST prime where the simple counting argument breaks.

### The escape hatch (not yet proved)

Higher-weight zero-sums exist (the η bound guarantees weight ≤ p). With weight W > 4 and support m > 4: the product Π(S_j+1) grows. If ANY zero-sum has weight ≥ p-1, the lift works. But proving that such a high-weight zero-sum always exists among 9 arc-forming points in F_p³ is an OPEN PROBLEM.

### Verdict

**The 8-tail bound is proved for p ≤ 13 (where 2^{support} ≥ p). For p ≥ 17, the lift without e₁ has a genuine gap.** The proof chain breaks here.

Possible fix: prove that among 9 non-proportional vectors in F_p³, there always exists a zero-sum of weight ≥ p-1 (or that the union of achievable first-coordinate values, across ALL zero-sums, covers F_p). Neither is trivial.

---

## ATTACK 2: THE "THREE-LINE ARGUMENT" FOR SHADOW SATURATION IS WRONG

**Target:** The claimed proof that η(C_p³) = 8(p-1)+1 implies Σ_{≤p-1}(A₈) = F_p³ \ {0}.

**The claim (Cortex entry 19d0b30ce1a):** "Shadow saturation proved via three-line argument from η definition."

### The bug

For nonzero v not proportional to any a_i ∈ A₈: add -v to get 9 non-proportional vectors. The η bound gives a zero-sum:

    Σ s_i a_i + s₉(-v) = 0,   Σs_i + s₉ ≤ p

So Σ s_i a_i = s₉ v, giving **s₉v ∈ Σ_{≤p-s₉}(A₈) ⊆ Σ_{≤p-1}(A₈)**.

But we want **v**, not s₉v. To recover v: v = s₉⁻¹ · (Σ s_i a_i) = Σ (s_i · s₉⁻¹) a_i. The weight of this representation is Σ⟨s_i · s₉⁻¹⟩, which is **NOT** equal to (Σs_i)/s₉. The rescaling by s₉⁻¹ changes each coefficient mod p independently.

**Example:** p = 7, s₁ = 3, s₂ = 2, s₉ = 2. Rescaled: s₁' = 3·4 = 12 ≡ 5 (mod 7), s₂' = 2·4 = 8 ≡ 1. New weight = 5+1 = 6 > original weight (3+2)/2 = 2.5.

**Σ_{≤p-1}(A₈) is NOT closed under scalar multiplication.** The three-line argument proves s₉v ∈ shadow, not v ∈ shadow.

### Why the conclusion is still true (by a DIFFERENT argument)

Shadow saturation for A₈ follows from the **Window Structure Theorem** + **Gap Hypothesis**:

1. The gap of Σ_{p-1}(A₈) is exactly {(0,j,j) : 1 ≤ j ≤ (p-3)/2}.
2. By the Window Theorem, (0,j,j) ∈ Σ_{2j}(A₈) for j ≤ (p-3)/2, and 2j ≤ p-3 < p-1.
3. All other nonzero v ∈ Σ_{p-1}(A₈).
4. Therefore Σ_{≤p-1}(A₈) = F_p³ \ {0}. ✓

But this route depends on the **Gap Hypothesis**, which is computationally verified but NOT analytically proved for all p.

### Verdict

**The three-line argument is invalid.** The correct proof route (Window + Gap) introduces a dependency on the unproved Gap Hypothesis. The proof chain's claim of "PROVED" shadow saturation should be downgraded to "CONDITIONAL on Gap Hypothesis."

---

## ATTACK 3: SHADOW SATURATION IS A₈-SPECIFIC, NOT UNIVERSAL

**Target:** The proof chain requires shadow saturation for ALL strongly ZSF 8-sets, not just A₈.

### The problem

At p = 5: there are **4 GL(3,F₅) classes** of strongly ZSF 8-sets (confirmed by prior adversary rounds). The Window Structure Theorem is proved **only for A₈'s specific coordinate representation**. The proof uses:

- The EXACT matrix entries of A₈ (coordinates of all 8 vectors)
- The specific linear constraints C1, C2 derived from coord1 = 0, coord2 = coord3 = j
- The parity argument from c₀ ≥ 0 ∧ c₁ ≥ 0

For a non-A₈ class: the invariant line L_B might be DIFFERENT, the constraints might not reduce the same way, and the window formula might have a different shape.

### The theorist's "Universal Window" conjecture

The theorist conjectured that every strongly ZSF 8-set B has an invariant line L_B with the same window structure. This is:

1. **Unproved** — no general argument exists
2. **Not even computationally verified** for all 4 GL classes at p = 5
3. **Structurally non-obvious** — different GL classes have different symmetry groups, different invariant lines, and potentially different window shapes

### Impact on the proof chain

If shadow saturation fails for even ONE GL class of strongly ZSF 8-sets, the GRAIL fails. The proof chain claims:

    doubled structure forced → tails form ZSF 8-set B → shadow saturation for doubled(B) → 18th vector killed

Step 3 requires shadow saturation for ALL possible B, not just A₈.

### Verdict

**The proof must either (a) prove A₈ uniqueness for all p ≥ 7, or (b) prove shadow saturation for all GL classes.** Neither is done. At p = 5, option (a) is FALSE (4 classes exist). Option (b) requires extending the Window Theorem to all classes.

---

## ATTACK 4: THE APPROACH IS NOT TRULY INDUCTIVE

**Target:** The research goal asks for ALL ranks r ≥ 3. The current work handles only r = 4.

### The false promise of induction

The proof outline claims an inductive structure:

    η(C_p^r) proved → 8-tail bound at rank r+1 → doubled structure → shadow saturation → η(C_p^{r+1})

But each step requires RANK-SPECIFIC structural analysis:

| Step | Rank 4 (from rank 3) | Rank 5 (from rank 4) | General rank r+1 |
|------|---------------------|---------------------|-----------------|
| Tail bound | 9 tails in F_p³ → rank-3 thm | 18 tails in F_p⁴ → rank-4 thm | α(r)+1 tails → rank-r thm |
| Doubled structure | 8 tails × 2 + e₁ | 17 tails × 2 + e₁ | α(r) tails × 2 + e₁ |
| Shadow saturation | Window for A₈ in F_p³ | Window for ?? in F_p⁴ | Window for ?? in F_p^r |
| Gap hypothesis | Gap of A₈ in F_p³ | Gap of ?? in F_p⁴ | Gap of ?? in F_p^r |
| ZSF classification | 4 GL classes at p=5 | Unknown | Unknown |

**The tail bound propagates cleanly** (each rank uses the previous rank's theorem). **Everything else requires new work at each rank.**

### The real obstruction

At rank r, the extremal strongly ZSF sets have size α(r) = 9·2^{r-3} - 1, which grows exponentially. Understanding the structure of these sets (their invariant lines, window formulas, gap hypotheses) becomes exponentially harder. There is no reason to believe the A₈ analysis generalizes.

### Verdict

**The current approach proves η(C_p⁴) at best, not η(C_p^r) for all r.** A truly inductive proof would need a RANK-INDEPENDENT argument for shadow saturation — one that doesn't depend on the specific structure of the rank-r extremal set.

---

## ATTACK 5: SELF-CONSISTENT ORBIT COVERAGE UNPROVED FOR LARGE j

**Target:** The 18th-vector closure for v = (0, b) with b on the gap line L.

### The gap

For b = (0,j,j) with j ∈ {(p+3)/2, ..., p-1}: the theorist needs w ∈ {1,...,p-1} such that wj mod p ∈ [⌈w/2⌉, 2⌊w/2⌋]. This is a number-theoretic question about multiplicative orbits hitting intervals.

**Proved:** j ≤ (p-1)/2 (direct substitution at w = p-1).
**Proved:** j = (p+1)/2 (at w = 2).
**Unproved:** j ∈ {(p+3)/2, ..., p-1}.

### Why the heuristic doesn't close

The counting argument: total window area ≈ (p-1)²/4, each orbit element appears once per w. Expected hits per target ≈ (p-1)/4. For p ≥ 5, this exceeds 1. But:

1. This is an AVERAGE, not a minimum. Some j values might have 0 hits.
2. The character sum error term O(√p log p) is the same ORDER as the expected value for small p.
3. The interval [⌈w/2⌉, 2⌊w/2⌋] has size ≈ w/2, which varies with w. Small w gives tiny intervals.

### Concrete concern at p = 5

j ∈ {4}: need w with 4w mod 5 ∈ [⌈w/2⌉, 2⌊w/2⌋].

- w=1: 4·1=4, interval [1,0] = ∅. ✗
- w=2: 4·2=3, interval [1,2]. 3 ∉ [1,2]. ✗
- w=3: 4·3=2, interval [2,2]. 2 ∈ {2}. ✓

So j=4 works at w=3. But this required checking — it's not guaranteed by any general argument.

### Verdict

**Moderate gap.** The orbit coverage is likely true for all p (verified through p=31) but proving it requires either (a) an explicit construction for each j, or (b) a character sum estimate with explicit constants. Neither exists.

---

## SUMMARY: PROOF CHAIN STATUS

```
Step 1: No-tripled-tails                    [PROVED ✓]
Step 2: 8-tail bound                        [PROVED for p ≤ 13; GAP for p ≥ 17 ✗]
Step 3: Doubled structure forced             [DEPENDS on Step 2]
Step 4: Tails form ZSF 8-set                [PROVED ✓ (given doubled structure)]
Step 5: Shadow saturation for doubled(B)     [CONDITIONAL on Gap Hypothesis + Universal Window ✗]
Step 6: 18th-vector closure                  [CONDITIONAL on Steps 5 + Orbit Coverage ✗]
Step 7: η(C_p⁴) = 17(p-1)+1                [CONDITIONAL on Steps 2-6]
Step 8: Induction to rank r                  [NO MECHANISM for shadow saturation at rank r ✗]
```

### What I could NOT break

| Claim | Status |
|-------|--------|
| No-tripled-tails theorem | SOLID — clean analytic proof |
| Tail Invariance Theorem | SOLID — clean analytic proof |
| Window Structure for A₈ | SOLID — verified my own derivation, no errors |
| Gap Hypothesis (computational) | SOLID through p=53, likely true for all p |
| Lower bound η ≥ (9·2^{r-3}-1)(p-1)+1 | SOLID — Lean-verified |

### Priority for the theorist

1. **[CRITICAL]** Fix the 8-tail bound for p ≥ 17. Either prove a high-weight zero-sum always exists among 9 arc-forming points, or find an alternative lift argument that doesn't require e₁.

2. **[HIGH]** Prove the Gap Hypothesis analytically. The Window Theorem + explicit solution families from the adversary's prior work provide all the tools. The K=1 off-L case reduces to a feasibility problem with ~5 integer constraints.

3. **[HIGH]** Prove Universal Window or A₈ uniqueness for p ≥ 7. Either extends the proof to all strongly ZSF 8-sets.

4. **[MODERATE]** Prove self-consistent orbit coverage for j > (p+1)/2.

5. **[STRUCTURAL]** Find a rank-independent shadow saturation argument for the general induction.

---

## Scripts

None this round. Pure theory.
