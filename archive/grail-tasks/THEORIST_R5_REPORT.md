# THEORIST ROUND 5 — REPORT

## HEADLINE: Two-Nonzero-Fiber Gap Identified and Partially Closed; Affine Hyperplane Case PROVED; Integer Weight Realization Remains Open

---

## Summary of New Results

| # | Result | Status | Method |
|---|--------|--------|--------|
| A | Fiber bounds (a) and (b) | **PROVED** | Inductive η/s constants |
| B | Two-nonzero-fiber gap identification | **PROVED** | Counting (b)+(b) = tight) |
| D | Shadow surjectivity mod p | **PROVED** | Linear algebra (rank of augmented matrix) |
| F | Cross-fiber weight decomposition | **PROVED** | Modular arithmetic on fiber constraint |
| H | Affine hyperplane ⟹ contradiction | **PROVED** | Linear form switching trick |
| I | Two-nonzero-fiber partial bound | **CONDITIONAL** | Integer weight realization unresolved |
| - | Always-zero-fiber lemma | **FALSE** | General position counterexample |
| - | Plotkin/GV integer weight bound | **INSUFFICIENT** | Exponential gap between code and ball |

---

## Theorem A: Fiber Bounds (PROVED)

**Setup.** Inductive hypothesis: η(C_p^r) ≤ α(r)(p−1)+1, hence s(C_p^r) ≤ (α(r)+1)(p−1)+1. Let S ⊂ F_p^{r+1} be ZSF with |S| = 2α(r)+2 non-proportional nonzero vectors. Fix linear form w with fibers F_c.

**(a)** |F_0| ≤ α(r).

*Proof.* F_0 ⊂ ker(w) ≅ F_p^r. Non-proportionality inherited. If |F_0| ≥ α(r)+1: sequence length |F_0|(p−1) ≥ α(r)(p−1)+(p−1) ≥ η(C_p^r). Get zero-sum of weight ≤ p within ker(w), lifting to F_p^{r+1}. Contradicts ZSF. ∎

**(b)** |F_c| ≤ α(r)+1 for c ≠ 0.

*Proof.* Vectors (c, u_i) in F_c have distinct projections u_i (since c ≠ 0 forces λ = 1 for proportionality). Within-fiber zero-sums have weight ≡ 0 (mod p), minimum p. If |F_c| ≥ α(r)+2: sequence length ≥ (α(r)+2)(p−1) ≥ (α(r)+1)(p−1)+1 = s(C_p^r). Get zero-sum of weight p. Contradicts ZSF. ∎

---

## Theorem B: The Two-Nonzero-Fiber Gap (PROVED — STRUCTURAL)

**Claim:** Part (c) of the coordinator's "Theorem 1" — that S spans ≥ 3 fibers — does NOT follow from (a)+(b) alone.

*Proof.* Three cases for ≤ 2 nonempty fibers:

1. **One fiber:** |S| ≤ max(α(r), α(r)+1) < 2α(r)+2. ✗
2. **F_0 ∪ F_c (c ≠ 0):** |S| ≤ α(r) + (α(r)+1) = 2α(r)+1 < 2α(r)+2. ✗
3. **F_{c₁} ∪ F_{c₂} (both nonzero):** |S| ≤ (α(r)+1)+(α(r)+1) = 2α(r)+2 = |S|. **No contradiction.**

The third case has TIGHT bounds: both fibers at maximum size α(r)+1. This is the genuine gap.

**Within nonzero fibers, all zero-sums have weight ≥ p** (since c·ΣS_i ≡ 0 ⟹ Σs_i ≡ 0, min p). So within-fiber zero-sums cannot have weight < p. Cross-fiber zero-sums face coupled constraints (Theorem F). ∎

---

## Theorem D: Shadow Surjectivity Mod p (PROVED)

**Theorem.** Let U = {u₁,...,u_m} ⊂ F_p^r with m ≥ r+1. If U does NOT lie in any affine hyperplane {ℓ = 1} (no linear form ℓ satisfies ℓ(u_i) = 1 for all i), then for every w ∈ F_p and every target t ∈ F_p^r, there exist s₁,...,s_m ∈ F_p with Σs_i ≡ w (mod p) and Σs_i u_i = t.

*Proof.* The map Φ: F_p^m → F_p^r × F_p, s ↦ (Σs_i u_i, Σs_i) has matrix:

    M = [u₁ u₂ ··· u_m]    (r × m)
        [1  1  ··· 1   ]    (1 × m)

rank(M) = r+1 iff (1,...,1) ∉ rowspan([u₁|···|u_m]).

(1,...,1) ∈ rowspan ⟺ ∃λ ∈ F_p^r: λᵀu_i = 1 ∀i ⟺ U ⊂ {ℓ = 1} for ℓ = λᵀ.

By hypothesis, no such ℓ exists. So rank(M) = r+1, Φ is surjective. ∎

**Corollary.** Σ_w(U) = F_p^r for every w ∈ F_p (modular weight).

**Caveat.** This is MODULAR: Σs_i ≡ w (mod p). The INTEGER weight could be w+kp for k ≥ 0.

---

## Theorem F: Cross-Fiber Weight Decomposition (PROVED)

**Setup.** S = F₁ ∪ F_c with c ∈ F_p\{0,1}, WLOG c₁ = 1. Projections U₁, U_c ⊂ F_p^r.

**Theorem.** A cross-fiber zero-sum of total weight w ∈ {1,...,p} requires fiber weights (W₁, W₂) uniquely determined by:
- W₂ ≡ −w/(c−1) (mod p)
- W₁ = w − W₂ (mod p)
- W₁ + cW₂ ≡ 0 (mod p) [first coordinate constraint]

The zero-sum exists iff Σ_{W₁}(U₁) ∩ (−Σ_{W₂}(U_c)) ≠ ∅ (shadows intersect at complementary targets).

*Proof.* Zero-sum: Σs_i(1,u_i) + Σt_j(c,u'_j) = 0. First coord: W₁ + cW₂ ≡ 0. Projection: Σs_iu_i = −Σt_ju'_j. Since c ≠ 1: W₂ = −w/(c−1) is unique given w.

The weight split (W₁, W₂) is determined. A solution exists iff some t lies in both Σ_{W₁}(U₁) and −Σ_{W₂}(U_c). ∎

**Weight feasibility.** For c ≠ p−1: there exists w* ∈ {1,...,p−1} with W₁+W₂ < p as integers. (Averaging: Σ_{W₁=1}^{p-1} (W₁ + ⟨−cW₁⟩) = p(p−1). If constant = p for all W₁, then c = p−1. Otherwise some value < p.)

For c = p−1: W₁ + W₂ = p for all w. Cross-fiber weight is always exactly p. Still ≤ p.

---

## Theorem H: The Affine Hyperplane Trick (PROVED — KEY NEW RESULT)

**Theorem.** If the projection set U₁ (or U_c) lies in an affine hyperplane {ℓ = 1} ⊂ F_p^r, then S is NOT ZSF.

*Proof.* Suppose U₁ ⊂ {ℓ = 1} for some linear form ℓ: F_p^r → F_p.

Define the linear form w̃ = ℓ∘π − w on F_p^{r+1}, where π is projection to the last r coordinates.

For v = (1, u_i) ∈ F₁: w̃(v) = ℓ(u_i) − w(v) = 1 − 1 = 0.

So ALL α(r)+1 vectors of F₁ lie in ker(w̃) ≅ F_p^r.

By Theorem A(a), the zero fiber under w̃ can hold at most α(r) non-proportional vectors. But |F₁| = α(r)+1 > α(r). By the inductive η-bound, there exists a zero-sum of weight ≤ p among these vectors.

This zero-sum lives in ker(w̃) ⊂ F_p^{r+1}, so it IS a zero-sum in F_p^{r+1}. Contradiction with ZSF. ∎

**Symmetric version.** Same argument for U_c ⊂ {ℓ' = 1}: define w̃' = c·ℓ'∘π − w, getting w̃'(c, u'_j) = c·1 − c = 0. Same contradiction. ∎

**Impact.** This eliminates the affine hyperplane sub-case of the two-nonzero-fiber problem. The remaining case is when NEITHER U₁ NOR U_c lies in any affine hyperplane.

---

## The Remaining Gap: Integer Weight Realization

**Status.** In Case 3 (neither projection set in an affine hyperplane), Theorem D gives mod-p surjectivity: Σ_{W₁}(U₁) = F_p^r for every W₁ ∈ F_p. Combined with Theorem F, this gives a MODULAR zero-sum: there exist coefficients with the right modular weight.

**The obstruction:** The integer weight Σs_i (with s_i ∈ {0,...,p−1}) could be W₁+kp for k ≥ 0. We need k = 0 (integer weight = W₁ ≤ p−1 or = p if c = p−1).

**Why standard bounds fail:**
- **Plotkin:** Average integer weight = m(p−1)/2 ≫ p. Bounding weight ≤ p removes only ~p/m fraction.
- **Gilbert-Varshamov:** Kernel has p^d elements, weight-≤-p ball has ~C(m+p,p) elements. Both are much smaller than p^m. No forced intersection.
- **Pigeonhole on forms:** Average |F_0| ≈ N/p ≈ 4. Need α(r)+1 = 9. Not enough.

**The integer weight realization is a GENUINELY NEW problem** not covered by standard coding theory or additive combinatorics.

---

## Failed Approach: Always-Zero-Fiber Lemma

**Proposed:** For any S with |S| = 2α(r)+2, there exists w* with |F_0^{w*}| ≥ α(r)+1.

**Disproved.** Take 2α(r)+2 vectors in general position (no r+1 linearly dependent). Every hyperplane contains ≤ r of them, so |F_0^{w*}| ≤ r < α(r)+1 for all w*.

This is a geometric obstruction: sets in "general position" avoid large intersections with any hyperplane.

---

## The Inductive Closure (Conditional)

**Theorem (Conditional Inductive Step).** Assume:
- (IH) η(C_p^r) ≤ α(r)(p−1)+1
- (TNFC) Two-Nonzero-Fiber Conjecture
- (MFC) Multi-Fiber Conjecture: ≥ 3 fiber configurations of size 2α(r)+2 admit zero-sums of weight ≤ p

Then η(C_p^{r+1}) ≤ (2α(r)+1)(p−1)+1.

The **TNFC** is reduced to:

> **Integer Weight Realization Conjecture (IWRC):** For m ≥ r+2 non-proportional nonzero vectors {u_i} in F_p^r NOT lying in any affine hyperplane, and any target t ∈ F_p^r and w ∈ {1,...,p−1}, there exist s_i ∈ {0,...,p−1} with Σs_i u_i = t, Σs_i = w (INTEGER equality, not just mod p).

Note: IWRC is strictly stronger than needed for TNFC. For TNFC, we only need SOME w ∈ {1,...,p−1} to work, not ALL w. And we only need SOME target t in a specific intersection, not ALL t.

The **MFC** is the principal open problem (same as before).

---

## Proof Architecture

```
η(C_p^r) ≤ α(r)(p−1)+1              [INDUCTIVE HYPOTHESIS]
  ↓ Theorem A(a)
|F_0| ≤ α(r)                         [PROVED]
  ↓ Theorem A(b)
|F_c| ≤ α(r)+1, c ≠ 0               [PROVED]
  ↓ Counting
{F_0, F_c} two-fiber impossible       [PROVED — counting gap]
  ↓ Theorem H
{F_{c₁}, F_{c₂}} with U in aff.hyp   [PROVED — form switching]
  ↓ Theorem D + F
{F_{c₁}, F_{c₂}} mod-p zero-sum      [PROVED — surjectivity]
  ↓ IWRC (OPEN)
{F_{c₁}, F_{c₂}} integer zero-sum    [CONDITIONAL]
  ↓ MFC (OPEN)
≥ 3 fibers zero-sum                   [OPEN — principal gap]
  ↓ Conclusion
η(C_p^{r+1}) ≤ α(r+1)(p−1)+1        [CONDITIONAL on IWRC + MFC]
```

---

## Directives for Other Agents

### COMPUTER
**Primary:** Test the Integer Weight Realization Conjecture (IWRC).

[VERIFY: For p = 5, 7, 11: take m = 9 random non-proportional nonzero vectors in F_p^3 NOT lying in any affine hyperplane. For each w ∈ {1,...,p−1}: check whether Σ_w(U) = F_p^3 (INTEGER weight exactly w, not mod p). Count failures. Run 1000 random trials.]

[VERIFY: For p = 5, 7: construct the "hardest" two-nonzero-fiber configuration — 9 vectors in F₁ and 9 in F_c, c ∈ {2,...,p−2} — and check if a cross-fiber zero-sum of weight ≤ p exists. Exhaustive over all such configurations (or large random sample).]

### ADVERSARY
**Primary:** Try to construct a counterexample to TNFC at p = 5. Specifically: find 18 non-proportional nonzero vectors in F_5^4 with values in {c₁, c₂} (both nonzero) under SOME linear form, such that NO zero-sum of weight ≤ 5 exists. This would break the proof.

**Secondary:** If no counterexample exists, try to identify which step of the proof (D, F, H, or integer weight) would need to fail for a counterexample to exist.

---

## Key Insights for Cross-Pollination

### For COMPUTER
The affine hyperplane trick (Theorem H) is computationally checkable: for each candidate ZSF set in two nonzero fibers, check whether the projection set lies in {ℓ = 1} for some ℓ. If yes, the set CANNOT be ZSF (by Theorem H). This may eliminate many candidates without exhaustive zero-sum search.

### For ADVERSARY
The integer weight gap is the PRECISE weakness to target. If you can find vectors where Σ_w(U) = F_p^r mod p but Σ_w(U) ⊊ F_p^r at integer weight w, this demonstrates the gap is real (not just theoretical). The adversarial configuration would have: (i) projections not in any affine hyperplane, (ii) cross-fiber zero-sums only at modular weight w+p (not w), (iii) w+p > p, so weight ≤ p fails.

### For THEORIST (self)
The most promising path to close IWRC: prove that among the p^{d} solutions to Φ(s) = (t, w mod p) in the kernel coset, at least one has Hamming support ≤ w (hence integer weight ≤ w(p−1), which is too large) — OR use the specific structure of ZSF projections (they are extremal ZSF sets in F_p^r by the inductive hypothesis) to constrain the integer weight.

The shadow saturation approach from the adversary's report (prove covering radius ≤ p−1 for the kernel code) remains the most promising bypass for BOTH the TNFC and MFC simultaneously. If Σ_{≤p-1}(S) = F_p^{r+1} \ {0} for any maximal ZSF set S, then adding ANY vector to S creates a zero-sum of weight ≤ p.
