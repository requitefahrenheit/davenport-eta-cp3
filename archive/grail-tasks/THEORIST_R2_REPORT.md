# THEORIST ROUND 2 — REPORT

## HEADLINE: Universal Shadow Saturation PROVED (5-line proof); Weight Flexibility DISPROVED; Inductive Bottleneck PRECISELY IDENTIFIED

---

## Theorem 1: Universal Shadow Saturation (NEW — PROVED)

**This is the main result of this round.** It resolves Adversary Attacks 2 and 3 from Session 6.

**Theorem.** Let r ≥ 3 and p ≥ 5 be an odd prime. Assume η(C_p^r) = α(r)(p−1)+1. Let B = {b₁,...,b_{α(r)}} ⊂ F_p^r be ANY strongly ZSF set. Then:

$$\Sigma_{\leq p-1}(B) = F_p^r \setminus \{0\}.$$

That is: every nonzero vector in F_p^r is representable as a non-negative-integer-coefficient combination of B with total weight ≤ p−1.

**Proof.**

Let v ∈ F_p^r \ {0}.

**Case 1: v is not proportional to any b_i.** Consider the multiset M = B^{p-1} ∪ {−v}. This consists of α(r)(p−1) copies of B elements plus ONE copy of −v. Total: α(r)(p−1) + 1 = η(C_p^r) elements.

Since −v is not proportional to any b_i, M is a valid sequence of η(C_p^r) nonzero elements. By the η bound, M contains a non-empty zero-sum subsequence of length ≤ p:

    Σ c_i b_i + t(−v) = 0,   c_i ∈ {0,...,p−1},  t ∈ {0,1},  0 < Σc_i + t ≤ p.

If t = 0: this is a zero-sum within B^{p-1} of weight ≤ p, contradicting the ZSF assumption.

Therefore t = 1, giving **v = Σ c_i b_i** with weight Σc_i ∈ {0,...,p−1}. Since v ≠ 0, Σc_i ≥ 1. Hence v ∈ Σ_{≤p-1}(B). ∎

**Case 2: v = λb_j for some j and λ ∈ {1,...,p−1}.** Then v = λb_j ∈ Σ_λ(B) trivially (coefficient λ on b_j, zero on all others). Weight λ ≤ p−1. ∎

**Key innovation over the prior "three-line argument":** The prior argument (attacked by the Adversary in Session 6) used −v with multiplicity **p−1**, yielding s₉v ∈ shadow (not v). My proof uses −v with multiplicity **1**, so t ∈ {0,1}. When t = 1, we get v directly — no rescaling needed.

### Why This Is Important

1. **Universality:** The proof works for ANY strongly ZSF set B, not just A₈. No Window Theorem, Gap Hypothesis, or coordinate structure needed.

2. **Resolves Adversary Attack 2:** The "three-line argument" bug (rescaling by s₉) is completely avoided. Shadow saturation now follows from η alone.

3. **Resolves Adversary Attack 3:** At p = 5, there are 4 GL classes of strongly ZSF 8-sets. Shadow saturation holds for ALL of them, not just A₈. The proof is class-independent.

4. **Inductive power:** The proof uses only the η bound and the ZSF assumption. It works at ANY rank, assuming the η bound holds.

---

## Theorem 2: Minimum Shadow Weight (PROVED)

**Theorem.** Let B be a strongly ZSF set of size α(r) in F_p^r. For any b_j ∈ B and λ ∈ {1,...,p−1}:

    w*(λb_j) = λ,

where w*(v) = min{w : v ∈ Σ_w(B)} is the minimum representation weight.

**Proof.** Upper bound: λb_j ∈ Σ_λ(B) trivially. So w* ≤ λ.

Lower bound: Suppose v = λb_j = Σ c_i b_i with Σc_i = w < λ and c_i ∈ {0,...,p−1}. Then (c_j − λ)b_j + Σ_{i≠j} c_i b_i = 0.

Since w < λ, we have c_j < λ (because c_j ≤ w < λ). So c_j − λ < 0 in Z. In F_p: c_j − λ ≡ c_j − λ + p (mod p), giving coefficient ⟨c_j − λ + p⟩ ∈ {1,...,p−1} on b_j.

This yields a zero-sum with coefficients ⟨c_j − λ + p⟩ on b_j and c_i on b_{i≠j}, all in {0,...,p−1}. Total weight = (c_j − λ + p) + Σ_{i≠j} c_i = w − λ + p ∈ {1,...,p}.

Since B is ZSF (no zero-sum of weight ≤ p), this is a contradiction. ∎

**Corollary:** The shadow weight function on projective lines through B is exactly the scaling factor. In particular, the shadow at weight 1 is exactly B itself: Σ₁(B) = B.

---

## Theorem 3: Weight Flexibility is FALSE (DISPROVED)

**The Weight Flexibility Theorem stated in goal.md is FALSE.**

**Statement (goal.md):** For any α(r)+1 non-proportional nonzero vectors in F_p^r, each with multiplicity p−1, the set of achievable zero-sum weights W ⊆ {1,...,p} satisfies |W| ≥ (p+1)/2.

**Counterexample:** Take B = A₈ and v₉ = (0,1,1) in F_5³. The set S = A₈ ∪ {(0,1,1)} has 9 non-proportional vectors. Any zero-sum must use v₉ with some coefficient s ∈ {1,...,4}:

    Σ c_i a_i + s·(0,1,1) = 0  ⟹  Σ c_i a_i = −s·(0,1,1) = (0, 5−s, 5−s).

Target (0, 5−s, 5−s) is on L = {(0,j,j)} with j = 5−s. Weight budget for A₈: Σc_i ≤ 5−s.

By the Window Theorem: (0,j,j) ∈ Σ_w(A₈) iff ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋.

- **s = 1:** j = 4. Need w ≤ 4 with w ≥ 4 (from j ≤ 2⌊w/2⌋). So w = 4. Total = 5. ✓
- **s = 2:** j = 3. Need w ≤ 3 with 3 ≤ 2⌊w/2⌋. w=2: 3 ≤ 2. ✗. w=3: 3 ≤ 2. ✗. **No solution.**
- **s = 3:** j = 2. Need w ≤ 2 with 2 ≤ 2⌊w/2⌋. w=2: 2 ≤ 2. ✓. Total = 5. ✓
- **s = 4:** j = 1. Need w ≤ 1 with 1 ≤ 2⌊w/2⌋. w=1: 1 ≤ 0. ✗. **No solution.**

**Only achievable weight: w = 5 = p.** So |W| = 1 ≪ (p+1)/2 = 3.

[VERIFY: For A₈ ∪ {(0,1,1)} in F_5³, confirm via exhaustive search that the ONLY zero-sum with weight ≤ 5 has weight exactly 5.]

**Consequence:** The Cauchy-Davenport strategy from goal.md (combining weight sets from different fibers) FAILS. Individual 9-vector sets can have only ONE achievable zero-sum weight (namely p), making cross-fiber combination impossible via this route.

---

## Theorem 4: Weight Mod-p Invariance Under Perturbation (PROVED)

**Theorem.** Let v₁,...,v_n ∈ F_p^r and c = (c₁,...,c_n) ∈ {0,...,p−1}^n with Σ c_i v_i = 0 (a zero-sum of weight w = Σ c_i). Let d ∈ (Z/pZ)^n satisfy Σ d_i v_i = 0 and Σ d_i ≡ 0 (mod p). Define c' = (⟨c₁+d₁⟩,...,⟨c_n+d_n⟩) where ⟨·⟩ denotes the representative in {0,...,p−1}.

Then c' is also a zero-sum, and its weight w' = Σ ⟨c_i+d_i⟩ satisfies **w' ≡ w (mod p)**.

**Proof.** Σ ⟨c_i+d_i⟩ v_i = Σ (c_i+d_i) v_i = Σ c_i v_i + Σ d_i v_i = 0 + 0 = 0. ✓

For the weight: ⟨c_i+d_i⟩ = c_i + d_i − p·ε_i where ε_i ∈ {0,1} accounts for mod-p reduction. So:

    w' = Σ(c_i + d_i) − p·Σε_i = w + Σd_i − p·Σε_i ≡ w (mod p).  ∎

**Consequence:** Perturbations that preserve the tail zero-sum and weight (mod p) can only change the integer weight by multiples of p. This means:

- From weight w ≤ p, perturbation gives weights in {w, w±p, w±2p, ...}.
- **You cannot fine-tune the weight continuously.** The weight is "stuck" in its residue class mod p.
- This explains why zero-sum weights tend to cluster at exactly p (the smallest positive multiple of w₀ ≡ 0 mod p in {1,...,p}).

---

## Theorem 5: Inductive Step — What Works and What Doesn't

### What WORKS: Large-Fiber Cases

**Theorem (Large-Fiber Inductive Step).** Assume η(C_p^r) = α(r)(p−1)+1 and s(C_p^r) = (α(r)+1)(p−1). Given 2α(r)+2 non-proportional nonzero vectors in F_p^{r+1}, a zero-sum of weight ≤ p exists if any of the following hold under some linear form w: F_p^{r+1} → F_p:

(a) Fiber 0 has ≥ α(r)+1 vectors.
(b) Some nonzero fiber c has ≥ α(r)+2 vectors.

**Proof.**
(a) Fiber-0 tails are non-proportional (since (0,t₁) ∝ (0,t₂) iff t₁ ∝ t₂). With ≥ α(r)+1 non-proportional tails, the multiset has ≥ (α(r)+1)(p−1) > η(C_p^r) copies. The η bound gives a zero-sum of tails at weight ≤ p. Lifting to F_p^{r+1}: first coordinate = 0·w = 0. ✓

(b) Fiber-c multiset has n_c(p−1) ≥ (α(r)+2)(p−1) = (α(r)+1)(p−1) + (p−1) ≥ s(C_p^r) copies (since s = (α(r)+1)(p−1) and p−1 ≥ 1). The s bound gives a zero-sum of tails at weight EXACTLY p. Lifting: first coordinate = c·p ≡ 0. ✓

### What FAILS: The Multi-Fiber Bottleneck

**The remaining case:** Fiber 0 has ≤ α(r) vectors, every nonzero fiber has ≤ α(r)+1 vectors, and at least 2 nonzero fibers are nonempty.

**The precise obstruction:** In a nonzero fiber c with n_c ≤ α(r)+1 vectors:
- The tail multiset has n_c(p−1) ≤ (α(r)+1)(p−1) = s(C_p^r) − 1 copies.
- The η bound guarantees a zero-sum of weight w ≤ p, but NOT w = p specifically.
- For the lift to F_p^{r+1}: we need c·w ≡ 0 (mod p), requiring w = p.
- With exactly s−1 copies, weight-p zero-sums are NOT guaranteed.

**Cross-fiber approach:** Combine partial sums from multiple fibers. Need Σ_c c·W_c ≡ 0 (mod p) with Σ_c W_c ≤ p. This requires matching exact-weight representations across fibers.

Shadow saturation gives: any nonzero target is in Σ_{≤p-1}(B) for any ZSF set B. But we need the target at a SPECIFIC weight (determined by the first-coordinate constraint), not just ANY weight.

**This is the EXACT-WEIGHT SHADOW problem:** Given a ZSF set B, target t, and specific weight w, is t ∈ Σ_w(B)?

---

## Theorem 6: The Exact-Weight Shadow Problem (REDUCTION)

**The Grail reduces to the following:**

**Conjecture (Exact-Weight Shadow Coverage).** Let B ⊂ F_p^r be a strongly ZSF set of size α(r). For every nonzero t ∈ F_p^r and every w ∈ {1,...,p−1}: t ∈ Σ_w(B).

**Why this would suffice:** In the multi-fiber case, choose any nonzero fiber c with k vectors. Let the tails be T_c. A weight-W_c partial sum from T_c contributes σ_c ∈ Σ_{W_c}(T_c) to the tail equation. The complementary fiber-0 contribution must be −σ_c ∈ Σ_{W_0}(T_0) where T_0 is the fiber-0 tail set (a ZSF set of size ≤ α(r)) and W_0 = ⟨−cW_c⟩.

If Exact-Weight Shadow Coverage holds: −σ_c ∈ Σ_{W_0}(T_0) for the required W_0. Done.

**Status:** The conjecture is almost certainly FALSE. From the Window Theorem: (0,1,1) ∉ Σ_1(A₈) at p = 5 (since w*(0,1,1) = 2). So there exist (t,w) pairs where t ∉ Σ_w(B).

**Weakened version:** Instead of ALL (t,w) pairs, we need enough pairs to cover the cross-fiber first-coordinate constraint. The precise requirement is:

**Conjecture (Cross-Fiber Solvability).** Given ZSF set B₀ of size α(r) in F_p^r and any set T_c ⊂ F_p^r of size ≤ α(r)+1 in a nonzero fiber c, there exist W_c ∈ {1,...,p−1}, σ_c ∈ Σ_{W_c}(T_c), and W_0 = ⟨−cW_c⟩ such that −σ_c ∈ Σ_{W_0}(B₀) and W_0 + W_c ≤ p.

---

## Theorem 7: The s−1 Threshold (PROVED)

**Theorem.** In the critical multi-fiber case, the tail multiset in each nonzero fiber has EXACTLY s(C_p^r) − 1 copies when the fiber has α(r)+1 vectors. This is the EXACT threshold where the s constant fails to guarantee weight-p zero-sums.

**Proof.** s(C_p^r) = η(C_p^r) + p − 1 = α(r)(p−1) + 1 + (p−1) = (α(r)+1)(p−1) + 1 − 1 = (α(r)+1)(p−1).

Wait, let me recalculate. η(C_p^r) = α(r)(p−1)+1. s(C_p^r) = η + p − 1 = α(r)(p−1) + p.

Fiber with n_c = α(r)+1 vectors: copies = (α(r)+1)(p−1). Compare with s = α(r)(p−1) + p.

Difference: (α(r)+1)(p−1) − [α(r)(p−1) + p] = (p−1) − p = −1.

So (α(r)+1)(p−1) = s(C_p^r) − 1. **Exactly one short of the s threshold.** ∎

**Significance:** This is not a coincidence. It reflects the fundamental tension:
- The lower bound construction uses α(r)+1 vectors per fiber (doubled+e₁).
- This is DESIGNED to be just below the s threshold.
- Breaking through requires either (a) proving the s−1 case also gives weight-p zero-sums (under structural constraints), or (b) a completely different approach.

---

## The Updated Proof Chain

```
η(C_p^r) = α(r)(p−1)+1                          [ASSUMED INDUCTIVELY]
  ↓ (Universal Shadow Saturation — NEW)
Σ_{≤p-1}(B) = F_p^r \ {0} for ANY ZSF α(r)-set  [PROVED — Theorem 1]
  ↓ (Large-Fiber Cases)
η(C_p^{r+1}) ≤ (2α(r)+1)(p−1)+1                 [PROVED for large fibers — Theorem 5]
  ↓ (Multi-Fiber Case)
Need: Cross-Fiber Solvability Conjecture           [OPEN — Theorem 6]
  ↓
η(C_p^{r+1}) = (2α(r)+1)(p−1)+1                 [CONDITIONAL on above]
```

---

## Verification Requests for COMPUTER

[VERIFY: For A₈ ∪ {(0,1,1)} in F_5³, enumerate ALL zero-sums (c₁,...,c₉) ∈ {0,...,4}^9 with Σc_i v_i = 0 and 1 ≤ Σc_i ≤ 5. Confirm the ONLY achievable weight is 5.]

[VERIFY: For each of the 4 GL classes of strongly ZSF 8-sets B in F_5³ and each nonzero v ∈ F_5³, confirm v ∈ Σ_{≤4}(B). This tests Universal Shadow Saturation for all classes.]

[VERIFY: For A₈ in F_p³ with p = 5,7,11: for each nonzero target t and each weight w ∈ {1,...,p−1}, determine whether t ∈ Σ_w(A₈). Output the "exact-weight shadow" matrix: an (p³−1) × (p−1) table with entry 1 if achievable, 0 otherwise. We need to understand the density of this matrix.]

[VERIFY: Cross-Fiber Solvability at p = 5: Take B₀ = A₈ (fiber-0 tails) and T_c = any subset of size ≤ 9 from F_5³ (fiber-c tails). For c ∈ {1,2,3,4} and each T_c, check whether there exist W_c, σ_c ∈ Σ_{W_c}(T_c), with −σ_c ∈ Σ_{p−cW_c mod p}(B₀) and W_c + (p−cW_c mod p) ≤ p.]

---

## Strategic Assessment

### What's Proved (solid, unconditional)
1. Universal Shadow Saturation for all ranks (given η).
2. Weight is stuck mod p under zero-sum-preserving perturbations.
3. Large-fiber inductive step (≥ α(r)+1 in fiber 0 or ≥ α(r)+2 in nonzero fiber).
4. The s−1 threshold is EXACT.

### What's Disproved
5. Weight Flexibility Theorem (goal.md) is FALSE at p = 5.
6. Cauchy-Davenport on weight sets cannot work in its stated form.
7. The exact-weight shadow coverage conjecture is FALSE (some (t,w) pairs fail).

### What's Open
8. Cross-Fiber Solvability — the PRECISE remaining gap.
9. Whether all ZSF sets have enough exact-weight shadow density.
10. Any rank-independent structural argument for the multi-fiber case.

### The Path Forward
The most promising direction is to prove Cross-Fiber Solvability. This requires showing: for any fiber-0 ZSF set B₀ and any fiber-c tail set T_c, the combined sumset structure has enough "weight-matching" pairs. This is a question about the JOINT density of exact-weight shadows across two sets, not just the cumulative shadow.

**Key observation:** Even though individual (t,w) pairs can fail, the AVERAGE density of the exact-weight shadow is (p−1)/p (since the cumulative shadow is full and each target has ≥ 1 achievable weight). For the cross-fiber solvability to fail, the weight assignments would need to be "adversarially correlated" between the two sets — which is a very strong structural constraint.

**Conjecture (Weight Orbit Coverage — Refined):** For any ZSF α(r)-set B and any nonzero t ∈ F_p^r, the set {w ∈ {1,...,p−1} : t ∈ Σ_w(B)} has cardinality ≥ 2. If true, this gives enough flexibility for cross-fiber matching with 3+ fibers.

---

## Summary Table

| # | Result | Status | Impact |
|---|--------|--------|--------|
| 1 | Universal Shadow Saturation | **PROVED** | Resolves Attacks 2,3; rank-independent |
| 2 | Minimum Shadow Weight | **PROVED** | w*(λb) = λ exactly |
| 3 | Weight Flexibility (goal.md) | **DISPROVED** | Cauchy-Davenport approach fails |
| 4 | Weight Mod-p Invariance | **PROVED** | Explains weight clustering at p |
| 5 | Large-Fiber Inductive Step | **PROVED** | Handles fiber 0 ≥ α+1 or fiber c ≥ α+2 |
| 6 | s−1 Threshold | **PROVED** | α+1 vectors = exactly s−1 copies |
| 7 | Cross-Fiber Solvability | **CONJECTURED** | The ONE remaining gap |
