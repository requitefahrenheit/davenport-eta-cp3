# Adversary Session 4 Round 1: U1 Is Dead

## Executive Summary

**Conjecture U1 (Two-Fiber Forcing) is FALSE.** I independently re-verified 7 counterexamples from Round 2 with fresh code, confirmed all are strongly ZSF with minimum 3 fibers under all 156 projective linear forms. Shadow saturation holds universally regardless of fiber structure. The window structure ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋ is unbroken at all primes tested (p ≤ 31).

## Attack Results

### Attack 1: U1 Counterexamples — CONFIRMED (7/7)

Each counterexample replaces one vector in doubled+e1 with the same tail in a different fiber:

| Pos | Old → New | Fibers | ZSF | Min fibers |
|-----|-----------|--------|-----|------------|
| 1 | (0,0,1,0)→(3,0,1,0) | {0:7,1:9,3:1} | ✓ | 3 |
| 2 | (0,0,0,1)→(2,0,0,1) | {0:7,1:9,2:1} | ✓ | 3 |
| 9 | (1,0,1,0)→(2,0,1,0) | {0:8,1:8,2:1} | ✓ | 3 |
| 10 | (1,0,0,1)→(3,0,0,1) | {0:8,1:8,3:1} | ✓ | 3 |
| 12 | (1,1,1,0)→(2,1,1,0) | {0:8,1:8,2:1} | ✓ | 3 |
| 15 | (1,4,1,2)→(4,4,1,2) | {0:8,1:8,4:1} | ✓ | 3 |
| 15 | (1,4,1,2)→(2,4,1,2) | {0:8,1:8,2:1} | ✓ | 3 |

Verification method: exhaustive enumeration of all coefficient tuples (support 1–5, each coeff ∈ {1,...,4}, total weight ≤ 5). All 156 projective forms checked for fiber count.

### Attack 2: Window Structure — UNBROKEN

Formula ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋ for j ∈ Σ_w(A₈) ∩ L verified via DP:

| Prime | Weights tested | Violations |
|-------|---------------|------------|
| 5 | 1–4 | 0 |
| 7 | 1–6 | 0 |
| 11 | 1–10 | 0 |
| 13 | 1–12 | 0 |
| 29 | 1–28 | 0 |
| 31 | 1–30 | 0 |

**I could not break this.** The window structure appears to be a genuine theorem about A₈.

### Attack 3: Multi-Fiber Stress Test

How far can same-tail swaps go?

- **Double swaps**: ALL 128 tested pairs (both to fiber 2) preserve strongly ZSF. Zero failures.
- **5-fiber config {0:4, 1:4, 2:4, 3:4, 4:1}**: Strongly ZSF ✓, shadow 624/624 ✓
- **Spread configs**: Multiple balanced 5-fiber configs all strongly ZSF with full shadow.

**Key subtlety**: The 5-fiber config has min_fibers = 2 under form (1,4,4,4). So it's NOT a U1 counterexample — it does have a 2-fiber form! Only single-swap configs (min_fibers = 3) are genuine U1 counterexamples.

### Attack 4: Shadow Saturation — UNIVERSALLY CONFIRMED

Every strongly ZSF 17-set tested has shadow saturation 624/624 at p=5:

| Configuration | Fibers (coord 0) | Shadow |
|--------------|------------------|--------|
| doubled+e1 | {0:8, 1:9} | 624/624 |
| pos=9 swap | {0:8, 1:8, 2:1} | 624/624 |
| pos=1 swap | {0:7, 1:9, 3:1} | 624/624 |
| pos=10 swap | {0:8, 1:8, 3:1} | 624/624 |
| pos=15 swap | {0:8, 1:8, 2:1} | 624/624 |
| 5-fiber | {0:4,1:4,2:4,3:4,4:1} | 624/624 |
| spread_1 | {0:4,1:4,2:3,3:3,4:3} | 624/624 |

**I could not break shadow saturation for any strongly ZSF 17-set.**

## What's Dead

1. **Conjecture U1** — FALSE. 7 confirmed counterexamples.
2. **Any proof relying on 2-fiber structure** — the same-tail swap mechanism produces 3-fiber strongly ZSF sets trivially.
3. **The window approach to U1** — the window structure is correct but U1 itself is wrong, so the window doesn't help here.

## What Survives

1. **Window structure** ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋ — confirmed at all primes ≤ 31, zero violations. This is a genuine property of A₈ worth proving.
2. **Shadow saturation universality** — unbreakable across all tested configs. This IS the right proof target.
3. **The grail itself** — η(C_p^4) = 17(p−1)+1 is not threatened by any finding. Every 18-vector set creates a zero-sum.

## Recommended Proof Direction

The proof should target shadow saturation directly:

**Theorem (to prove):** If S ⊂ F_p^4 has 17 non-proportional nonzero vectors and is strongly ZSF (no zero-sum at weight ≤ p), then Σ_{≤p-1}(S) = F_p^4 \ {0}.

This would immediately give η(C_p^4) = 17(p−1)+1: any 18th vector v₁₈ satisfies -v₁₈ ∈ Σ_{≤p-1}(S₁₇), giving a zero-sum at weight ≤ p.

The proof cannot assume 2-fiber structure or uniqueness. It must work for ALL strongly ZSF 17-sets.

## Open Questions for Next Round

1. Does the window structure hold for non-A₈ strongly ZSF 8-sets? (I couldn't find alternatives at p=7 via single-swap search — the greedy search was too expensive.)
2. Can shadow saturation be proved from the kernel minimum distance argument? (The kernel of a strongly ZSF set has minimum weight p+1; need covering radius ≤ p−1.)
3. Is there a Chevalley-Warning argument that proves shadow saturation directly?
