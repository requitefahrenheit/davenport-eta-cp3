# Shadow Window Structure and Two-Fiber Forcing (U1)
## Discoveries from Session 4, March 20, 2026

---

## 1. The Problem

**Conjecture U1 (Two-Fiber Forcing):** Every strongly ZSF set of maximal
size 2α(r)+1 in F_p^{r+1} lives in at most 2 hyperplane fibers.

Equivalently: if a set of 2α(r)+1 nonzero vectors in F_p^{r+1} uses 3+
fibers (under any hyperplane projection), then it has a zero-sum of
weight ≤ p.

---

## 2. The Shadow Window Structure (NEW)

**Theorem (computational, verified p ≤ 23).**
Let A₈ be the 8-vector construction in F_p³. On the invariant line
L = {(0, j, j) : j ∈ F_p*}, the value j is in Σ_w(A₈^{p-1}) if and
only if

    ⌈w/2⌉ ≤ j ≤ 2⌊w/2⌋.

Explicitly:
- w = 2k (even): covered values are {k, k+1, ..., 2k}
- w = 2k+1 (odd): covered values are {k+1, k+2, ..., 2k}

The window has width ⌊w/2⌋ + 1 (even) or ⌊w/2⌋ (odd), and its left
endpoint advances by 1 every 2 weight steps.

**Consequences:**
- Gap at weight p-1: exactly {(0,j,j) : 1 ≤ j ≤ (p-3)/2}, size (p-3)/2.
- Cumulative shadow Σ_{≤p-1} = F_p³ \ {0} (Shadow Saturation) — the
  windows tile the full range as w goes from 2 to p-1.
- The gap sits entirely on the fixed-point line of the (2↔3) coordinate
  symmetry of A₈, which maps a₁↔a₂, a₄↔a₅, a₆↔a₇ and fixes a₀, a₃.

**Why this matters for U1:** With 2 fibers, the 2-Fiber Elimination
theorem blocks ALL cross-fiber zero-sums at weight ≤ p. With 3 fibers,
cross-fiber zero-sums are possible at weight < p. The window structure
tells us exactly which cross-fiber zero-sums exist at each weight, and
different weights cover each other's gaps.

---

## 3. Sumset Completeness (NEW)

**Observation (verified p ≤ 23):**
For A₈ and all j + k ≤ p-1:

    Σ_j(A₈) + Σ_k(A₈) = Σ_{j+k}(A₈)

where the left side is the sumset of independent copies.

This means the shadows are "splitting-closed": a vector reachable at
weight j+k can always be decomposed as a weight-j part plus a weight-k
part (using independent copies of A₈).

**Consequence:** The cross-fiber argument using two full fibers (each
containing A₈) gains NO additional coverage from independence. The
sumset of two copies at weights j and k is exactly the shadow at j+k
of a single copy.

---

## 4. P-Independent Shadow Sizes (NEW)

For p ≥ 2w + 1 (no modular wraparound):

| w | |Σ_w(A₈)| | Stabilizes at p ≥ |
|---|----------|-------------------|
| 1 | 8        | 5                 |
| 2 | 30       | 5                 |
| 3 | 77       | 7                 |
| 4 | 159      | 11                |
| 5 | 286      | 11                |
| 6 | 468      | 13                |
| 7 | 715      | 17                |

The shadow sizes at small weights are determined by the INTEGER linear
algebra of A₈ (coordinates in {-2,-1,0,1,2}), independent of p.

---

## 5. Computational Verification of U1

### 5a. The (α, α, 1) distribution

For fibers {0, 1, c} with A₈ in fibers 0 and 1, and one extra vector
b in fiber c:

**Result:** For p = 5, 7, 11, for ALL fiber labels c ∈ {2,...,p-1} and
ALL nonzero vectors b, the 3-fiber configuration has a zero-sum of
weight ≤ p.

**Mechanism:** Two complementary mechanisms cooperate:
1. **Weight-p cross-fiber (allocation (k, p-2k, k)):** Works for most
   (c, b) pairs. For fiber label c = 2 (and c = p-1), this kills all b.
   For other c values, 1-2 vectors survive.
2. **Weight-< p cross-fiber:** The survivors from mechanism 1 are ALL
   killed by cross-fiber zero-sums at weight < p. These exist because
   with 3+ fibers, the congruence W₁ + c·W_c ≡ 0 mod p can be
   satisfied with W₁ + W_c < p.

The 2-Fiber Elimination theorem blocks BOTH mechanisms for 2-fiber
configurations: W₁ ≡ 0 mod p forces W₁ = 0 or p at ALL weights.
With 3 fibers, this constraint is relaxed.

### 5b. All distributions

**Result:** For p = 5, 7, 11, U1 holds for the (α, α, 1) distribution
(the hardest case, verified exhaustively). Other distributions (α, α-k,
k+1) for k ≥ 1 have MORE extra vectors and MORE cross-fiber freedom,
making them easier.

---

## 6. Path to a Proof

### What needs to be proved:

**(A) Window Structure.** Prove that j ∈ Σ_w(A₈) ∩ L iff ⌈w/2⌉ ≤ j ≤
2⌊w/2⌋. This is a statement about the kernel parametrization of A₈
restricted to the invariant line. The constraints reduce to:

    c₀ - c₃ + c₄ + c₅ - c₆ - c₇ = 0     (first coord = 0)
    c₁ - c₂ + c₄ - c₅ + c₆ - c₇ = 0     (2nd = 3rd coord)
    j = c₁ + c₃ + c₄ + 2c₆ + c₇          (value)
    Σ cᵢ = w                                (weight)
    0 ≤ cᵢ ≤ p-1                           (bounds)

The window pattern should follow from analyzing the feasible region of
this integer linear program.

**(B) Number-Theoretic Orbit Coverage.** For c = 2: prove that for all
m ∈ {1,...,p-1}, ∃ k ∈ {1,...,(p-1)/2} such that (-km mod p) falls in
the window [⌈(p-k)/2⌉, 2⌊(p-k)/2⌋]. This is a statement about
multiplicative orbits and interval coverage in F_p.

**(C) Lower-Weight Cross-Fiber.** For fiber labels c where the weight-p
argument leaves survivors: prove that weight-< p cross-fiber zero-sums
exist. The shadows at weight 2-3 are p-independent and can be
explicitly computed.

**(D) General A (beyond A₈).** Extend from A₈ to arbitrary maximal ZSF
sets. This requires either proving A₈ uniqueness (sub-problem U2) or
showing the shadow structure has enough generality.

### Difficulty assessment:

- (A) is an explicit integer programming exercise — TRACTABLE
- (B) is a number theory lemma — probably KNOWN or followable from
  standard equidistribution arguments
- (C) follows from (A) by explicit case analysis — TRACTABLE
- (D) is the hardest part and may require U2

---

## 7. Relationship to the Grail

If U1 is proved (for A₈), the proof chain becomes:

    η(C_p³) = 8(p-1)+1                   [PROVED]
    U2: A₈ is unique maximal ZSF          [OPEN — but strong evidence]
    U1: 3+ fibers impossible              [NEW: reduced to items A-C above]
    ↓
    Conjecture U                           [CONDITIONAL on U2]
    ↓
    η(C_p^{r+1}) = (2α(r)+1)(p-1)+1      [THE GRAIL, conditional on U]

The shadow window structure is the key new structural insight that
makes U1 tractable. It converts the combinatorial problem into a
number-theoretic problem about multiplicative orbits.
