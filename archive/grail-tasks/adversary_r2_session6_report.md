# ADVERSARY Round 2 Session 6 — Final Report

## HEADLINE: U2 IS DEAD. THE GRAIL SURVIVES.

Tail Uniqueness (U2) is false at p=7: a GL-inequivalent maximal strongly ZSF 8-set exists. However, this alternative set has *better* shadow properties than A8 and the Grail holds exhaustively for its doubled construction. The 4D shadow gap is real but unexploitable. Weight-decoupling permanently blocks fiber induction.

---

## Finding 1: U2 (TAIL UNIQUENESS) DISPROVED AT p=7

**Alternative maximal strongly ZSF 8-set:**
```
ALT = [(0,0,4), (0,3,0), (5,0,0), (6,0,4), (2,6,4), (2,6,1), (5,4,0), (1,6,4)]
```

**Exhaustive verification:**

| Property | A8 | ALT |
|---|---|---|
| Strongly ZSF (weight ≤ 7) | ✓ | ✓ |
| Exhaustively maximal (all 294 extensions) | ✓ | ✓ |
| Collinear triples | 4 | 6 |
| Per-point collinear distribution | [1,1,1,1,2,2,2,2] | [2,2,2,2,2,2,3,3] |
| |Σ₆| (shadow at weight p−1) | 340 (gap=2) | **342 (gap=0)** |
| GL(3,7)-equivalent | — | **NO** |
| Doubled+e₁ strongly ZSF 17-set | ✓ | ✓ |
| Grail (exhaustive, all 2298 vectors) | ✓ | **✓** |

**Key insight:** ALT has FULL shadow saturation (no gap at all). The Gap Hypothesis is A8-specific, not a universal property of maximal 8-sets. Despite this structural difference, the Grail holds identically.

**Impact:** The proof cannot assume U2. It must work for ANY maximal α-set.

---

## Finding 2: 4D SHADOW GAP — REAL BUT UNEXPLOITABLE

Σ_{p-1}(A8) in F_p³ misses exactly (p−3)/2 projective directions: {(0,j,j) : 1 ≤ j ≤ (p−3)/2}.

**Gap Hypothesis verified:** through p=53 (all primes), zero exceptions.

**4D targets (0,0,p−j,p−j) escape shadow saturation but are still killed:**

| Attack configuration | Mechanism that kills gap targets | Count |
|---|---|---|
| Standard doubled+e₁ | Support-3 collinear triples | 100% |
| Single fiber-0 swap (break 2/4 families) | Support-3 triples (remaining families) | 100% |
| Full fiber-0 swap (break all 4 families) | **Support-4 at weight exactly p** | 100% |
| Random fiber assignments (50K samples, p=5) | Support-4 (when all triples broken) | 100% |

**Zero counterexamples across all configurations tested.**

Two-mechanism structure: collinear triples handle most fiber configs; when all triples are broken, support-4 zero-sums at weight p provide backup.

---

## Finding 3: WEIGHT-DECOUPLING OBSTRUCTION (PROVED)

**Theorem:** If S ⊂ Fc = {v : w(v)=c} with c ≠ 0 and Σ aᵢvᵢ = 0 with aᵢ ≥ 1, then Σ aᵢ ≡ 0 (mod p), so the weight is exactly p.

**Proof:** 0 = w(Σ aᵢvᵢ) = c·Σaᵢ, and c ≠ 0 in F_p, so Σaᵢ ≡ 0 (mod p). With 1 ≤ aᵢ ≤ p−1 and weight ≤ p, this forces weight = p.

**Impact:** Fiber induction (decompose by fibers, apply lower-dimensional bound) cannot work directly. Nonzero-fiber zero-sums are invisible at weight < p. The proof needs a top-level argument (like shadow saturation) rather than fiber-by-fiber analysis.

---

## Attack Ledger

| Attack | Target | Outcome |
|---|---|---|
| U2 disproof search | Tail uniqueness | **BROKEN** — ALT exists at p=7 |
| ALT exhaustive maximality | ALT validity | CONFIRMED — all 294 extensions fail |
| ALT shadow saturation | Gap structure | ALT has NO gap (better than A8) |
| Doubled+ALT Grail test | Grail for non-A8 sets | HOLDS — all 2298 vectors killed |
| 4D shadow gap analysis | Shadow saturation | Gap real, all targets killed |
| Fiber-0 swap (2/4 families) | Collinear triple mechanism | Remaining families provide backup |
| Total collinear break (4/4) | All triple families | Support-4 at weight p fills gap |
| Random fiber search (50K) | Arbitrary fiber configs | Zero counterexamples |
| Weight-decoupling | Fiber induction approach | **BLOCKED permanently** |
| Gap Hypothesis large p | Shadow gap formula | Confirmed through p=53 |

---

## What Is Dead (cumulative)

1. **U1 (Two-Fiber Forcing)** — FALSE at all primes (Session 4)
2. **U2 (Tail Uniqueness)** — FALSE at p=7 (this session)
3. **Fiber induction** — blocked by weight-decoupling obstruction
4. **Sumset composition on L** — fails for large p (Session 4)

## What Survives All Attacks

1. **The Grail bound η(C_p⁴) ≤ 17(p−1)+1** — exhaustive at p=5,7 for BOTH A8 and ALT
2. **α(3,p) = 8** — no 9-element strongly ZSF set exists
3. **Doubling construction** — works for both A8 and ALT
4. **Tail Rigidity** — unbroken (Session 4)
5. **Window formula** — unbroken through p=53
6. **Gap Hypothesis for A8** — confirmed through p=53

---

## Recommendations for Theorist (Updated)

1. **Drop U2.** State all results for arbitrary maximal strongly ZSF α-sets. The doubling construction and Grail should be proved for any such set.

2. **Exploit ALT's full saturation.** If you can show that most/all maximal α-sets have full shadow saturation (like ALT), the 4D gap problem only arises for A8-like sets with specific algebraic structure.

3. **Two-mechanism Grail proof.** For sets WITH a shadow gap (like A8): prove that gap targets are killed by support-4. For sets WITHOUT a gap: shadow saturation directly implies maximality.

4. **Tail Rigidity is still the right structural invariant** (from Session 4). Even though U2 is false in 3D, Tail Rigidity in 4D remains unbroken: every strongly ZSF 17-set has tails matching some maximal 8-set (A8 or ALT or others).

5. **Don't use fiber induction.** Weight-decoupling makes this impossible. Use top-level shadow saturation instead.

---

## Files (this session)

- `adversary_r5_verify_alt.py` — Initial ALT verification (ZSF, collinear, GL-equivalence)
- `adversary_r5_alt_deep.py` — Exhaustive ALT analysis (maximality, shadow, doubled, Grail)
- `adversary_r5_shadow_gap.py` — 4D shadow gap discovery and analysis
- `adversary_r5_swap_gap.py` — Same-tail swap vs gap targets
- `adversary_r5_fiber0_swap.py` — Fiber-0 swap breaking 2/4 triple families
- `adversary_r5_total_break.py` — Breaking all 4 triple families simultaneously
- `adversary_r5_gap_p31.py` — Gap Hypothesis at p=31,37

## Cortex Entries

- `19d0fcce0ae-09fcb` — 4D shadow gap analysis
- `19d0fcf012b-159ee` — Weight-decoupling obstruction
- `19d0fe62686-18565` — U2 disproof and ALT verification
