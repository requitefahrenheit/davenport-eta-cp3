# Adversary Report: Round 1 of 3

**Date:** 2026-03-21
**Role:** ADVERSARY — break things, find obstructions, construct near-misses

---

## Finding 1: Pair-Degenerate Weight Bound (PROVED)

**Statement:** For any collinear triple with a pair-degenerate dependency (α, β, γ) — meaning some pair of coefficients sums to 0 — the minimum achievable weight is **exactly p+1**, strictly exceeding the budget p.

**Proof:** WLOG γ = 1. Three sub-cases:

- **α = −1:** W(μ) = ⟨−μ⟩ + ⟨μβ⟩ + ⟨μ⟩ = (p − ⟨μ⟩) + ⟨μβ⟩ + ⟨μ⟩ = p + ⟨μβ⟩ ≥ p + 1
- **β = −1:** W(μ) = ⟨μα⟩ + (p − ⟨μ⟩) + ⟨μ⟩ = p + ⟨μα⟩ ≥ p + 1
- **α = −β:** W(μ) = ⟨−μβ⟩ + ⟨μβ⟩ + ⟨μ⟩ = p + ⟨μ⟩ ≥ p + 1

**Impact:** The rank-3 theorem is the ONLY support-3 tool. It requires non-degeneracy. Pair-degenerate triples contribute NOTHING to the weight ≤ p budget. Any configuration where all collinear triples are pair-degenerate is immune to support-3 attacks.

---

## Finding 2: Fiber Pigeonhole Ratio Kills Induction at ≥ 3 Fibers (PROVED)

**Statement:** The ratio (α(r)+2)/(α(r−1)+1) = (2α(r−1)+3)/(α(r−1)+1) is always strictly less than 3. For r ≥ 4, it's less than 2.38.

**Consequence:** With ≥ 3 nonempty fibers and α(r)+2 vectors, Pigeonhole guarantees max fiber size ≤ ⌊(α(r)+2)/3⌋ < α(r−1)+1. Within-fiber induction via η or s constants NEVER fires.

**Why the two-fiber case works:** With 2 fibers, Pigeonhole gives max(a,b) ≥ ⌈(α(r)+2)/2⌉ = α(r−1)+2 > α(r−1)+1. So one fiber always has enough for η (fiber 0) or s (fiber c). This is a CLIFF at exactly 3 fibers.

**Explicit failure at rank 5:** 36 vectors across 3 fibers (12+12+12). Each fiber has 12 projections in F_p⁴. Need 18 for η(C_p⁴). Gap of 6. Unfixable.

---

## Finding 3: Cap Obstruction Blocks ALL Support-3 (PROVED)

**Statement:** The maximum cap size in PG(n−1, F_p) (no three collinear) is ≥ p² + 1 for n = 4 (Barlotti-Panella theorem, 1955). Confirmed by literature search:

- **PG(3, F_5):** cap size = 26
- **PG(3, F_7):** cap size = **50** (elliptic quadric)
- **PG(4, F_5):** cap size ≥ 66
- **PG(4, F_7):** cap size ≥ 132

Since α(4)+2 = 19 < 26 (p=5) and 19 < 50 (p=7), **18 points CAN be placed in PG(3, F_p) with no three collinear** for ALL p ≥ 5.

**Consequence:** There exist configurations of 18 non-proportional nonzero vectors in F_p⁴ where NO collinear triple exists at all. For such configurations, the rank-3 theorem and ALL support-3 arguments are completely useless. The same holds at rank 5 for p ≥ 7 (need 37 points, cap bound ≥ 50).

**Interaction with Finding 1:** Even configurations WITH collinear triples might have all of them pair-degenerate. Finding 1 shows these are equally useless. So the class of "support-3-immune" configurations is even LARGER than just caps.

---

## Finding 4: Support ≥ 4 Has No Working Tool (OBSERVED)

The dead ends establish:
- **Character theory for support 4:** Dead. Two energy levels instead of one. Cannot pin f₄(μ) to a single level.
- **Chevalley-Warning:** ~13 congruences in ~16 unknowns at rank 4. Underdetermined. Cannot show N > 0 alone.
- **Cross-fiber collinear triples:** 0/94 residual cases at p=5 had one. Wrong approach.

The 94 residual cases at p=5 were killed by **support-4 zero-sums of weight 4 < p = 5** (four vectors summing to zero with all coefficients = 1). No theoretical tool exists to GUARANTEE such zero-sums in general configurations.

This is the **core unsolved problem**: develop a theory for support ≥ 4 zero-sums of bounded weight.

---

## Finding 5: Fiber Decomposition Gives No Structural Gain (ARGUED)

A zero-sum s₁v₁ + ··· + sₖvₖ = 0 is r+1 equations in k unknowns (the sᵢ). Decomposing by fibers rewrites this as:
- r equations for the projection: Σ sᵢ · proj(vᵢ) = 0
- 1 equation for the fiber constraint: Σ sᵢ · cᵢ ≡ 0 (mod p)

This is just a reparametrization of the same r+1 equations. The fiber structure doesn't decouple or simplify the problem in the multi-fiber case.

In the two-fiber case, it works because the fiber constraint is trivially satisfied (pure fiber-0 zero-sums have Σ sᵢ · 0 = 0 automatically). With ≥ 3 fibers, the fiber constraint is non-trivial and couples to the projection equations.

---

## Lemma 2 Verification: Trivially True, Not Useful

The post-mortem's Lemma 2 (triple-sum-zero ⇒ weight = p achievable) follows from:

> **S(μ) + S(p−μ) = 3p** for all triples with α+β+γ ≡ 0.

Proof: ⟨x⟩ + ⟨p−x⟩ = p for all x ∈ F_p*. So each pair contributes p to the sum.

Since S(μ) ∈ {p, 2p}, if S(μ) = 2p then S(p−μ) = p. Choosing the right μ gives weight exactly p.

**But:** Weight = p, never < p. This is a boundary case. It confirms zero-sums exist but doesn't help find LIGHTER ones. And the sum-zero condition (α+β+γ = 0) with "no pair sums to 0" is AUTOMATICALLY satisfied whenever α,β,γ ∈ F_p* and α+β+γ = 0 (check: α+β = −γ ≠ 0, etc.).

---

## Adversary's Suggested Direction

The most promising path I see (as adversary, identifying what MIGHT work against my obstructions):

**Can the ZSF property force non-degenerate collinear triples to exist?**

If having α(r)+2 nonzero non-proportional vectors with NO zero-sum of weight ≤ p FORCES the existence of a non-degenerate collinear triple, then the rank-3 theorem applies and gives a contradiction.

The question reduces to: **Is every ZSF set of size α(r)+2 in F_p^{r+1} necessarily NOT a cap?**

At rank 4: is every 18-element ZSF set in F_p⁴ forced to have three collinear points? If yes, and if those points form a non-degenerate triple, the rank-3 theorem kills it. This would close the support-3 gap.

But I SUSPECT this is false: I believe caps can be ZSF. If so, support ≥ 4 theory is unavoidable.

---

## Obstruction Summary Table

| # | Finding | Status | What it kills |
|---|---------|--------|---------------|
| 1 | Pair-degenerate weight ≥ p+1 | PROVED | Support-3 for degenerate triples |
| 2 | Pigeonhole ratio < 3 | PROVED | Within-fiber induction for ≥ 3 fibers |
| 3 | Cap obstruction | PROVED | ALL support-3 for general-position configs |
| 4 | No support-4 tool | OBSERVED | Every current approach |
| 5 | Fibers = reparametrization | ARGUED | Hope that fiber structure simplifies multi-fiber |

---

## Literature Context (Web Search)

- **No published counterexample** to η(C_p^r) = (9·2^{r-3}−1)(p−1)+1 exists in the literature.
- **Davenport constant D(C_n^r) formula FAILS at rank ≥ 4** (Biswas-Mazumdar 2024, arXiv:2402.09999). Different invariant, but shows rank-2/3 patterns don't extend.
- **Girard-Schmid (2019-2020):** ti(G) > η(G) at rank 3 for C_2+C_2+C_{2n}. Structural theorems break qualitatively at rank 3.
- **Girard et al. (2025, arXiv:2510.23543):** Confirmed Gao's conjecture for "rank-two-like" p-groups. The boundary of their method may reveal where counterexamples live.
- **Ellenberg-Gijswijt cap bound** constrains s(F_p^n) from above. Connection to η is indirect but potentially useful.
- **Harborth constant** has a concrete counterexample in Z_3^3 (rank 3 failure for a related invariant).

**Key takeaway:** The conjecture is UNREFUTED but also UNPROVED beyond rank 3. The Davenport failure at rank 4 is cautionary — analogous conjectures CAN fail at higher ranks.
