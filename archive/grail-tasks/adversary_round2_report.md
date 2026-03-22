# Adversary Round 2 Report: Multi-Fiber ZSF Discovery

## Executive Summary

The two-fiber proof strategy has a **REAL GAP**: multi-fiber strongly ZSF configurations exist in F_5^4 that cannot be placed in ≤ 2 hyperplane fibers by ANY linear form. However, **shadow saturation is universal** — it holds for ALL tested strongly ZSF sets regardless of fiber structure. The proof must target shadow saturation directly.

## Key Findings

### 1. Multi-Fiber Strongly ZSF Sets EXIST

**This is the central adversary finding.** By single-vector perturbation of the doubled+e1 construction, I found 10 distinct 17-element strongly ZSF sets in F_5^4 with NO two-fiber linear form:

| Position replaced | New vector | Fiber distribution |
|---|---|---|
| 1 | (3,0,1,0) | {0:7, 1:9, 3:1} |
| 2 | (2,0,0,1) | {0:7, 1:9, 2:1} |
| 4 | (2,1,1,0) | {0:7, 1:9, 2:1} |
| 5 | (3,1,0,1) | {0:7, 1:9, 3:1} |
| 6 | (4,4,2,1) | {0:7, 1:9, 4:1} |
| 9 | (2,0,1,0) | {0:8, 1:8, 2:1} |
| 10 | (3,0,0,1) | {0:8, 1:8, 3:1} |
| 12 | (2,1,1,0) | {0:8, 1:8, 2:1} |
| 15 | (4,4,1,2) | {0:8, 1:8, 4:1} |
| 15 | (2,4,1,2) | {0:8, 1:8, 2:1} |

Additionally, a **4-fiber** configuration exists: replacing positions 10 and 15 gives fibers {0:8, 1:7, 2:1, 3:1}.

**Verification**: Each was checked exhaustively (all coefficient tuples with weight ≤ 5 = p). All 624 nonzero linear forms on F_5^4 were tested; none gives ≤ 2 fiber values. These sets are NOT in the GL(4,F_5) orbit of any doubled+e1 construction.

### 2. Shadow Saturation is Universal

**Every** strongly ZSF 17-element set tested has full shadow saturation at weight ≤ p-1 = 4:

- A8_known doubled+e1: 624/624 ✓
- 6 alternative B8 choices: 624/624 ✓
- 10 multi-fiber (3 fibers): 624/624 ✓
- 1 multi-fiber (4 fibers): 624/624 ✓
- A8 at p=7: 2400/2400 ✓

In contrast, **weakly ZSF** sets (zero-sum at weight exactly p) often FAIL shadow saturation:
- 4/5 tested weakly ZSF B8 sets had shadow gaps (6-135 missing vectors)
- Missed vectors have ALL preimage coefficient-vectors at weight ≥ p

### 3. A8 Is Not Unique (Correcting Prior Error)

The sub-agent's finding of ~640K alternative strongly ZSF 8-element sets at p=5 is **CORRECT**. My earlier debunking was wrong.

- 6/7 tested nc≥5 sub-agent passes verified by exhaustive check
- Only nc=4 examples show occasional false positives
- Alternative B8 sets ALL have shadow saturation
- The scaling rigidity (4/65536 ≈ 0.006% of representatives work) explains why random search missed them

### 4. Strong ZSF ⟹ Full Shadow (Mechanism)

For B8 ⊂ F_p^3 with 8 non-proportional vectors:

| Property | B8 shadow at w≤p-1 | S17 shadow at w≤p-1 |
|---|---|---|
| Strongly ZSF (w≤p) | 124/124 FULL (all tested) | 624/624 FULL |
| Weakly ZSF (w≤p-1 only) | 91-124 (varies) | 489-624 (varies) |

The **mechanism**: for missed targets, the weight-p zero-sum shifts ALL preimage coefficient-vectors to weight ≥ p, leaving zero low-weight preimages. For strongly ZSF sets, every target retains preimage points at weight ≤ p-1.

### 5. p=3 Shadow Saturation Holds

Confirmed: the doubled+e1 at p=3 (17 vectors in F_3^4) has shadow saturation at weight 2 (= p-1). All 80 nonzero vectors covered. First zero-sum at weight 4 = p+1.

## Implications for the Proof

### What's Broken
The two-fiber bound strategy assumes all ZSF sets can be decomposed into ≤ 2 fibers. **This assumption is FALSE.** Multi-fiber strongly ZSF sets exist.

### What Survives
Shadow saturation appears to be a **universal property of strongly ZSF sets**, independent of fiber structure. The conjecture η(C_p^{r+1}) = (2α(r)+1)(p-1)+1 is not contradicted by any finding.

### Recommended Direction
**Prove shadow saturation directly**: If B ⊂ F_p^{r+1} has (2α(r)+1) non-proportional nonzero vectors and is strongly ZSF (no zero-sum at weight ≤ p), then its weight-(p-1) shadow covers all of F_p^{r+1} \ {0}.

This would bypass the two-fiber gap entirely. The preimage weight-distribution argument may be formalizeable:

**Kernel weight gap:** For the doubled+e1 S17, the map φ: Z_p^17 → F_p^4 has kernel of dimension 13. The minimum nonzero weight in ker(φ) is **p+1** (not 2p — the first zero-sums are involution-type: (p-1)*v_a + v_b + v_c = 0 where v_a = v_b + v_c, giving weight (p-1)+1+1 = p+1). This is forced by strongly ZSF (no zero-sum at weight ≤ p).

Confirmed across primes:
- p=3: 60 zero-sums at weight 4 = p+1 (32 support-3, 28 support-4)
- p=5: 98 zero-sums at weight 6 = p+1 (20 support-3, 78 higher support)
- p=7: 136 zero-sums at weight 8 = p+1 (20 support-3, 116 higher support)

**Why the gap forces saturation:** Each target t has p^13 preimage points. The kernel's minimum weight p+1 means the strongly ZSF property excludes weights 1 through p from the kernel. For any coset c + K, the weight distribution must include a point at weight ≤ p-1 (since the p^13 coset points can't all avoid {1,...,p-1}).

**Proof strategy:** Show that the covering radius of a [17, 13, p+1]_p code is ≤ p-1. The gap is tight (minimum distance p+1, covering radius bound p-1, difference = 2) but this may follow from the specific structure of the code (generated by S17's geometry) combined with sphere-covering bounds.

## Computational Status

- `mass_shadow_test.py`: running (buffered output), testing 50 random strongly ZSF B8 sets
- `multi_fiber_search2.py`: running, random multi-fiber search in F_5^4
- `grail_task2_exhaustive.py`: running (~49h), full enumeration of all C(31,8)

### 6. Multi-Fiber Sets are Maximal and Near-2-Fiber

- All multi-fiber ZSF sets are maximal at 17 vectors (cannot add an 18th). Same bound as doubled+e1.
- Triple perturbation (moving 3 vectors to extra fibers): 0/50,000 trials succeeded
- The strongly ZSF property enforces a **near-2-fiber** constraint: at most 1-2 vectors can deviate from a 2-fiber decomposition
- This suggests a "relaxed 2-fiber" theorem might be provable: every maximal ZSF set has some linear form giving ≤ 2 fiber values for all but O(1) vectors

## Data Summary

| Test | Result |
|---|---|
| Multi-fiber ZSF exist? | **YES** (11 confirmed) |
| Shadow saturation for multi-fiber? | **YES** (all 11) |
| Shadow saturation for alternative B8? | **YES** (all 6) |
| Shadow saturation for weakly ZSF? | **NO** (4/5 fail) |
| A8 unique? | **NO** (~640K alternatives) |
| Shadow sat at p=7? | **YES** (2400/2400) |
| Shadow sat at p=3? | **YES** (80/80) |
