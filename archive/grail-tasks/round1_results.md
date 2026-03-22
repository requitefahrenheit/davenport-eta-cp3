# COMPUTER Agent — Round 1 Results

## Executive Summary

**Conjecture U1 (Two-Fiber Forcing) is FALSE at p=5.** However, a precise structural replacement has been identified: all counterexamples satisfy a **Line Concentration** property that may suffice for the proof strategy.

---

## Task B1: Window Structure at Large Primes ✓ VERIFIED

**Result:** Window conjecture verified computationally at p=29, 31, 37 (extending from p≤23).

For A8 in F_p^3 on L = {(0,j,j) : j ∈ F_p*}:

> j ∈ Σ_w(A8) iff ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋

- p=29: verified in 8.0s, shadow saturation FULL
- p=31: verified in 10.5s, shadow saturation FULL
- p=37: verified in 21.9s, shadow saturation FULL
- Analytical proof verified computationally for all primes 5 ≤ p ≤ 47

Gap at weight p−1 is exactly {(0,j,j) : 1 ≤ j ≤ (p−3)/2} for all tested primes.

**Files:** `window_verify_large_p.py`, `window_proof_verify.py`

---

## Task B2: (8,7,2) Distribution Verification — U1 DISPROVED

### Discovery of Counterexamples

The fixed verification (`verify_872_fixed.py` using set-based DP) initially found alleged counterexamples. Independent brute-force verification (`verify_counterexample.py`) confirmed:

- **3 of 6 initially tested CEs were false alarms** (collinear zero-sums missed by DP bug)
- **3 are GENUINE counterexamples** — confirmed ZSF by exhaustive enumeration AND ≥3 fibers under ALL 156 projective linear forms

### Complete Classification

Systematic scan revealed **324 genuine counterexamples** (36 subsets × 9 CEs each).

**Every counterexample has identical structure — "tail-replacement":**

1. Fiber 0: {(0, a) : a ∈ A8} — 8 vectors (unchanged)
2. Fiber 1: 7 of 9 standard vectors (drop any 2 indices i, j)
3. Extras: (c, a_i) and (c', a_j) for c, c' ∈ {2,3,4}

where a_i, a_j are the last-3-coordinates ("tails") of the dropped fiber-1 vectors.

**Key properties:**
- The extras are NOT scalar multiples of the dropped vectors: (c, a_i) ≠ c·(1, a_i)
- Under ALL 156 projective linear forms, the set uses ≥3 fibers (minimum 3, typical 4-5)
- Under tail projection π: (x₀,x₁,x₂,x₃) → (x₁,x₂,x₃), all CEs map to the SAME 9-point image as the standard construction

**Files:** `verify_counterexample.py`, `verify_872_fixed.py`, `verify_872_distribution.py` (buggy)

### Structural Insight: Line Concentration

All 324 counterexamples (and the standard construction) share the property:

> The 17 vectors lie on exactly 9 parallel lines in F_p^4, where each line has the form L_a = {(c, a) : c ∈ F_p} for a ∈ A8 ∪ {0}.

The standard construction samples each line at {c=0, c=1}. Counterexamples sample some lines at different fiber pairs (e.g., {c=0, c=2} or {c=1, c=3}).

---

## Modified Conjecture (Replaces U1)

**Conjecture U1' (Line Concentration):** Every strongly ZSF set of size 2α+1 in F_p^4 lies on at most α+1 parallel lines. Equivalently:

> There exists a linear projection π: F_p^4 → F_p^3 such that |π(S)| ≤ α+1 = 9.

**Why this may suffice for the proof:**
- If π(S) ⊆ A8 ∪ {0} (or a translate), the shadow analysis of A8 applies
- The gap structure at weight p−1 forces zero-sums when |S| > 2α+1
- The key property is not which fibers are used but that the projective spread is bounded

**What remains to prove:**
1. U1' holds for all maximal ZSF sets (not just tail-replacements of the standard construction)
2. The projection image is itself an extremal ZSF configuration in F_p^3
3. The inductive bound η(r+1) ≤ (2α(r)+1)(p−1)+1 follows from U1'

---

## Task B3: Non-A8 Maximal ZSF Sets — FOUND

**Result:** A8 is NOT the unique maximal ZSF 8-set in F_5^3. Found 200 maximal ZSF 8-sets across **5 invariant signature classes**, with only 14 (7%) GL-equivalent to A8.

| Signature | Count | GL-equiv to A8? |
|-----------|-------|-----------------|
| (4, (1,1,1,1,2,2,2,2)) | 14 | Yes (all 14) |
| (7, (2,2,2,3,3,3,3,3)) | 71 | No |
| (6, (1,2,2,2,2,3,3,3)) | 56 | No |
| (5, (1,1,2,2,2,2,2,3)) | 44 | No |
| (6, (2,2,2,2,2,2,3,3)) | 15 | No |

Example non-A8 set: {(0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,2), (1,2,2), (2,1,2)}

**Implication:** The modified conjecture U1' (Line Concentration) must be verified against 17-vector sets built from non-A8 bases, not just A8. The proof strategy cannot assume A8 is the only extremal configuration.

---

## Task B4: Sumset Completeness

**Result:** Σ_j(S) + Σ_k(S) = Σ_{j+k}(S) holds TRIVIALLY for ALL sets when j+k ≤ p−1, by the coefficient-splitting argument (any representation at weight j+k can be split into weight-j and weight-k parts). No computation needed.

---

## Bug Reports

1. **verify_872_distribution.py**: Uses min-weight DP where `min_wt[0] = 0` always (trivial zero-sum). All subsets falsely reported as having zero-sums.

2. **verify_872_fixed.py**: Set-based DP correctly detects SOME zero-sums but misses others (collinear zero-sums like 1·(0,1,0,1) + 3·(1,1,0,1) + 1·(2,1,0,1) = 0). The standalone DP code works correctly; the bug is specific to the script's subset construction or processing order.

---

## Computational Artifacts

| File | Purpose | Status |
|------|---------|--------|
| `window_verify_large_p.py` | Window at p=29,31,37 | ✓ Complete |
| `window_proof_verify.py` | Analytical proof check p≤47 | ✓ Complete |
| `verify_counterexample.py` | Brute-force CE verification | ✓ Complete |
| `verify_872_fixed.py` | Set-based DP (8,7,2) check | ⚠ Has subtle bug |
| `verify_872_distribution.py` | Min-weight DP check | ✗ Fundamentally buggy |

---

## Recommended Next Steps (Round 2)

1. **Build 17-vector sets from non-A8 bases**: The 4 non-A8 signature classes yield different 17-vector constructions in F_p^4. Check if they are ZSF and satisfy U1'.
2. **Verify U1' at p=5 exhaustively**: Check ALL maximal 17-vector ZSF sets (not just A8-based) for Line Concentration.
3. **Verify U1' at p=7**: Extend the analysis to the next prime.
4. **Complete B3 classification**: Determine the full number of GL-equivalence classes of maximal ZSF 8-sets at p=5 and p=7.
5. **Formalize the proof strategy**: Show how U1' + window structure + induction gives η(C_p^{r+1}).
