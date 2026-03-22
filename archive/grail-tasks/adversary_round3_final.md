# Adversary Round 3 — Final Report (Corrected)

## CRITICAL FINDING: A8 Non-Uniqueness

**A8 is unique ONLY at p=3.** At p≥5, multiple GL-inequivalent strongly ZSF 8-sets exist in F_p^3.

### p=3: Single GL(3,3) orbit (exhaustively verified)
- 117 projective classes × 6 scalings = 702 sets, ALL GL-conjugate to A8

### p=5: ≥4 distinct GL(3,5) classes
- 111 projective classes found (2000 greedy trials, likely many more)
- Distinguished by collinear triple count (GL invariant):
  - 4 triples: 7 projective classes (includes A8)
  - 5 triples: 35 projective classes
  - 6 triples: 49 projective classes
  - 7 triples: 20 projective classes

### p=7: 6 distinct GL(3,7) classes
- Confirmed by exhaustive GL equivalence check (background agent)
- 5 classes NOT equivalent to A8

## Same-Tail Swap Theorem (proved)

Replacing any vector (f, t) in doubled+e₁ with (f', t) for ANY f' ≠ f preserves
the strongly ZSF property (provided no proportional pair is created).

**Algebraic mechanism**: Every tail-equation solution at weight ≤ p using position j
is a twin-pair relation c·(f,t) + (p-c)·(f̄,t) = 0. The dangerous fiber is always
the partner fiber (∈ {0,1}), which is excluded by the proportionality constraint.

Verified exhaustively: p=5 (51/51), p=7 (85/85). Double swaps: p=5 (1200/1200).

## Consequences for Proof Strategy

### What is DEAD
1. **GL(4,p) uniqueness** of maximal strongly ZSF 17-sets — FALSE (swap theorem)
2. **Tail set uniqueness** up to GL(3,p) — FALSE (A8 non-uniqueness at p≥5)
3. **A8 uniqueness** in rank 3 — FALSE for p≥5
4. Any proof approach relying on structural uniqueness of maximal sets

### What STILL HOLDS
1. **Size bound**: All strongly ZSF 8-sets in F_p^3 are maximal at size 8
   (η(C_p^3) = 8(p-1)+1, Lean-verified)
2. **Fiber size bound**: No fiber can contain >8 non-proportional vectors (rank-3 theorem)
3. **All maximal strongly ZSF 17-sets are maximal at size 17** (verified at p=5,7)
4. **2-fiber elimination theorem**: Cross-fiber weight-p zero-sums impossible for 2-fiber sets
5. **Same-tail swap theorem**: Fiber assignments are flexible within doubled+e₁ framework

### Required proof approach
The proof of η(C_p^4) = 17(p-1)+1 needs a DIRECT argument:
- 18 non-proportional vectors in F_p^4 must have a zero-sum at weight ≤ p
- Cannot assume ANY structural uniqueness
- Must work with: fiber size ≤ 8 (rank-3 bound) + ≥3 fibers needed for 18 vectors
- Promising: polynomial method (Chevalley-Warning), fiber counting arguments
