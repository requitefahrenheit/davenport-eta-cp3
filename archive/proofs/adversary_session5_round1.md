# ADVERSARY SESSION 5 ROUND 1 — ALL FIVE APPROACHES HAVE NAMED OBSTRUCTIONS

## HEADLINE: Every proposed approach to the multi-fiber case has a precise, provable obstruction. The problem is harder than it looks. Shadow saturation remains empirically unbreakable but no theoretical tool is known to prove it.

---

## Attack 1: CHARACTER SUM AVERAGING IS PROVABLY DEAD AT SUPPORT ≥ 4

**The rank-3 trick**: For a 3-element dependency (a,b,c) with a+b+c ≡ 0 (mod p), define f_3(μ) = ⟨μa⟩ + ⟨μb⟩ + ⟨μc⟩. Since each ⟨μa_i⟩ ∈ {1,...,p-1} and f_3(μ) ≡ 0 (mod p), we have f_3(μ) ∈ {p, 2p}. The average:

$$\frac{1}{p-1}\sum_{\mu=1}^{p-1} f_3(\mu) = \frac{3 \cdot p(p-1)/2}{p-1} = \frac{3p}{2}$$

Since 3p/2 ∈ (p, 2p), some μ must have f_3(μ) = p. This is the engine of the rank-3 theorem.

**The support-4 obstruction**: For a 4-element dependency (a,b,c,d) with a+b+c+d ≡ 0 (mod p), define f_4(μ) = ⟨μa⟩ + ⟨μb⟩ + ⟨μc⟩ + ⟨μd⟩ ∈ {p, 2p, 3p}. The average:

$$\frac{1}{p-1}\sum_{\mu=1}^{p-1} f_4(\mu) = \frac{4 \cdot p(p-1)/2}{p-1} = 2p$$

**The average EQUALS the middle level.** The constant function f_4 ≡ 2p is consistent with the average. Therefore the averaging argument CANNOT force f_4(μ) = p for any μ.

**Explicit counterexample**: Take the dependency (1, 1, p-1, p-1). For any μ:

f_4(μ) = ⟨μ⟩ + ⟨μ⟩ + ⟨μ(p-1)⟩ + ⟨μ(p-1)⟩ = 2⟨μ⟩ + 2(p - ⟨μ⟩) = 2p

Weight 2p > p for ALL μ ∈ F_p*. No scaling achieves weight ≤ p.

**Consequence**: This dependency arises from v_1 + v_2 = v_3 + v_4 (non-proportional vectors forming a "parallelogram"). Such 4-tuples exist generically. Any proof that tries to find a low-weight support-4 zero-sum by character sum methods is dead.

**The general pattern**: For support k, the average is kp/2. This equals a level value (multiple of p) iff k is even. So:
- k = 3: average 3p/2, NOT a level → averaging works ✓
- k = 4: average 2p, IS a level → averaging fails ✗
- k = 5: average 5p/2, NOT a level → averaging works ✓ (but need support-5 dependencies, which are rare)
- k = 6: average 3p, IS a level → averaging fails ✗

**Even-support dependencies are immune to character sum averaging.**

---

## Attack 2: FIBER INDUCTION HAS A PERMANENT 3/2 GAP

**Setup**: At rank r+1, we have N = 2α(r)+2 vectors. Project to F_p^r via some linear form. Fiber induction requires at least one fiber to contain ≥ α(r)+1 non-proportional vectors.

**The obstruction**: With ≥ 3 non-empty fibers, the largest fiber has at most N - 2 = 2α(r) vectors. The inductive hypothesis needs α(r)+1. With a balanced 3-fiber split, each has ~(2α(r)+2)/3 vectors.

Needed per fiber: α(r) + 1 = (2α(r)+2)/2 = N/2
Available per fiber: (2α(r)+2)/3 = N/3

**Ratio: N/3 ÷ N/2 = 2/3. Each fiber has only 2/3 of what's needed. This gap is CONSTANT across all ranks.**

At rank 4: 18 vectors, need 9 per fiber, get 6 with 3 fibers. Gap = 3.
At rank 5: 36 vectors, need 18 per fiber, get 12 with 3 fibers. Gap = 6.
At rank 6: 72 vectors, need 36 per fiber, get 24 with 3 fibers. Gap = 12.

**The gap DOUBLES at each rank.** Fiber induction gets WORSE, not better, as rank increases.

**The cap obstruction (rank 4 specific)**: In PG(3, F_5), the maximum ovoid has 26 points, with at most p+1 = 6 points per hyperplane. So 18 points from an ovoid give at most 6 per hyperplane for ALL hyperplanes simultaneously. Fiber induction needs 9. This is a GEOMETRIC obstruction, not just a counting one.

(Caveat: caps at p=5 DO have zero-sums — the adversary in session claude-018 found all 113 are support-4 weight-5. So caps are not counterexamples to the main conjecture. But they ARE counterexamples to fiber induction as a proof method.)

**Verdict**: Fiber induction provably cannot handle the multi-fiber case at any rank.

---

## Attack 3: CHEVALLEY-WARNING CANNOT ENCODE THE WEIGHT CONSTRAINT

**The CW framework**: Variables s_1,...,s_n ∈ F_p. Polynomial system f_j(s) = Σ s_i v_{i,j} = 0 for j=1,...,r+1. CW says: if total degree of the system < n, then |solutions| ≡ 0 (mod p).

**The weight constraint problem**: We need Σs_i ≤ p (as an INTEGER), not Σs_i ≡ 0 (mod p). These are fundamentally different.

CW can encode "Σs_i ≡ c (mod p)" using the polynomial g_c(s) = 1 - (Σs_i - c)^{p-1}, degree p-1. Total degree: (r+1)·1 + (p-1) = r + p. For n = 2α(r)+2 = 18 at rank 4: CW requires r+p < 18, i.e., p < 14. Fine for small p.

**But CW gives**: N_c = |{s : Σs_iv_i = 0, Σs_i ≡ c \pmod{p}}| ≡ 0 (mod p).

This counts solutions with integer weight ∈ {c, c+p, c+2p, ...}. It CANNOT distinguish weight c from weight c+kp.

**Proof that this conflation is fatal**: Take the dependency (1,1,p-1,p-1) on 4 vectors. The "natural" solution s = (1,1,p-1,p-1) has weight 2p and residue 0 mod p. The only solutions are scalar multiples: μ·(1,1,p-1,p-1) with weight 2p for all μ. CW counts these and says N_0 ≥ p. But ALL solutions have weight 2p, not p. CW cannot detect this.

**The deeper issue**: Weight ≤ p is an ARCHIMEDEAN condition. F_p has no Archimedean structure — it's a finite field. The polynomial ring F_p[s_1,...,s_n] knows about modular arithmetic but not about integer size. No polynomial over F_p can encode "the integer lift of this sum is ≤ p."

**What about Reiher's approach?** Reiher proved s(Z_p^2) = 4p-3 using CW, but his situation was different: he had n = 4p-3 variables (scaling with p) and the relevant zero-sums had length exactly p (the s constant), avoiding the weight-distinction problem. For η, the weight can be anything from 1 to p, and CW conflates these with weights p+1 to 2p, etc.

**What about Grynkiewicz's weighted CW?** The weighted version (Combinatorica 2023) allows weighted polynomial constraints, but the weights are algebraic (in F_p), not integer-valued. The integer weight constraint Σs_i ≤ p remains non-algebraic. The weighted CW gives finer congruences on solution counts but still can't separate weight strata.

**Verdict**: The polynomial method (CW, Nullstellensatz, weighted CW) cannot encode the integer weight constraint that defines η. This is an intrinsic limitation, not a matter of technique.

---

## Attack 4: EXTREMAL NON-UNIQUENESS KILLS APPROACH 5

**Approach 5 proposed**: Assume α(r)+1 vectors are ZSF. Analyze the extremal structure. If the only extremal set is doubled+e_1, then α(r)+2 must break it.

**What's proved (Adversary R3)**: At p=5, there are **4 distinct GL(3,5) classes** of strongly ZSF 8-sets in F_5^3. Only one is A_8. The other three have different dependent-triple signatures (dep counts 5, 6, 7 vs A_8's 4).

**Each non-A_8 base produces valid doubled+B+e_1**: all are strongly ZSF with shadow saturation 624/624.

**Consequence**: Any proof that relies on "the extremal set is essentially unique" is FALSE. The proof must work for ALL GL classes simultaneously.

**Propagation to higher rank**: If there are 4 GL classes of ZSF 8-sets, the doubled+B+e_1 construction gives ≥ 4 classes of ZSF 17-sets. By the same reasoning, doubled+B_17+e_1 gives ≥ 4 classes of ZSF 35-sets at rank 5. **Non-uniqueness propagates inductively.**

**What survives**: Shadow saturation holds for ALL classes. The window formula holds for ALL classes (on set-specific invariant lines). So the proof target should be a UNIVERSAL property, not one tied to A_8's specific structure.

---

## Attack 5: THE INDUCTIVE FRAMEWORK HAS A CIRCULAR DEPENDENCY

**The proposed proof chain**:
1. Window formula for ZSF 8-sets in F_p^3 → Shadow saturation in F_p^3 → η(C_p^3)
2. η(C_p^3) → (somehow) → η(C_p^4)
3. η(C_p^4) → (somehow) → η(C_p^5)

**The circularity**: Step 2 requires proving shadow saturation at rank 4 (that Σ_{≤p-1}(S_17) = F_p^4 \ {0} for ZSF 17-sets S_17). But proving this requires either:
- (a) The window formula at rank 4 (which hasn't been established — it's only verified at rank 3)
- (b) The coding-theoretic argument (which faces the metric mismatch below)
- (c) A completely new approach

**The coding-theoretic metric mismatch**:

The kernel of a ZSF n-set in F_p^{r+1} is a linear [n, n-r-1, d≥p+1] code over F_p. Standard coding theory gives Hamming covering radius R_H ≤ n - (n-r-1) = r+1.

Shadow saturation needs: L1 covering radius ≤ p-1. With R_H ≤ r+1 nonzero coordinates, the L1 weight is at least R_H (all coefficients 1) and at most R_H·(p-1).

- Rank 4 (r+1=4): R_H ≤ 4 = p-1 at p=5. Need L1 ≤ 4. With ≤ 4 nonzero coords each ≥ 1: L1 ≥ R_H. If R_H = 4: need all coords = 1. **This requires that every syndrome is achieved by a UNIT coefficient vector of weight ≤ 4.** This is a much stronger condition than Hamming covering.

- Rank 5 (r+1=5): R_H ≤ 5. Need L1 ≤ 4 = p-1 at p=5. But R_H = 5 allows 5 nonzero coordinates, with L1 ≥ 5 > 4. **The Hamming bound is INSUFFICIENT at rank 5.**

**Consequence**: The coding-theoretic approach (min distance → covering radius → shadow saturation) works at rank 4 for p=5 ONLY IF every syndrome has a unit-weight-≤-4 representative. At rank 5, even the Hamming bound fails. At p=7 and rank 4: R_H ≤ 4 but p-1 = 6 ≥ 4, so Hamming works but L1 weight ≤ 6 with ≤ 4 coordinates allows non-unit coefficients, which is easier. The metric mismatch worsens specifically when r+1 > p-1.

---

## STRUCTURAL OBSERVATION: The "Parallelogram Obstruction"

The dependency (1,1,p-1,p-1) — corresponding to v_1 + v_2 = v_3 + v_4 — has weight 2p for all scalings. I call this the **parallelogram obstruction**: four non-proportional vectors forming a "parallelogram" in F_p^{r+1} cannot produce a zero-sum of weight ≤ p via their 4-element dependency.

**At p=5, rank 4**: Among the 94 residual cases, the killing zero-sums have fiber-weight decompositions (0,0,0,0), (1,1,1,2), (0,1,1,3), (0,0,1,4) — all summing to 0 mod 5 with total weight 0 or ≤ 4. None are of type (1,1,4,4).

**Question**: Among 18 non-proportional vectors in F_p^4, can ALL 4-element dependencies be parallelograms? If so, we'd need 5+ element zero-sums or 3-element zero-sums, and the problem reduces to:

(a) Finding a non-degenerate collinear triple (handled by rank-3 theorem), OR
(b) Finding a non-parallelogram 4-dependency, OR
(c) Finding a higher-support zero-sum of low weight

The cap construction avoids (a) entirely (no collinear triples). It avoids some (b). Does it always have (c)?

**For k=5** (odd support): the averaging argument gives average weight 5p/2, which lies strictly between 2p and 3p. So SOME μ gives weight ≤ 2p. But we need ≤ p. The average 5p/2 is above 2p, so averaging only gives weight 2p, not p.

Wait — let me recalculate. f_5(μ) ∈ {p, 2p, 3p, 4p}. Average 5p/2 ∈ (2p, 3p). So some μ gives f_5 ≤ 2p. That's weight ≤ 2p, NOT ≤ p. Averaging gives weight 2p at best.

**For k=p** (support p): f_p(μ) has average p²/2. The levels are {p, 2p, ..., (p-1)p}. Average p²/2 = p·(p/2). Since p/2 is not an integer for odd p, this lies strictly between levels ⌊p/2⌋·p and ⌈p/2⌉·p. Averaging gives weight ≤ ⌊p/2⌋·p ≈ p²/2. Still much larger than p.

**Conclusion**: Character sum averaging NEVER gives weight ≤ p for even support, and gives weight ≤ 2p (not ≤ p) for odd support ≥ 5. The averaging trick is fundamentally a rank-3 / support-3 tool.

---

## WHAT I COULD NOT BREAK

| Target | Attack method | Result |
|--------|---------------|--------|
| Shadow saturation | All prior attacks + new structural analysis | **UNBREAKABLE** |
| Window formula | Tested through p=43 and all 4 GL classes | **UNBREAKABLE** |
| Local tail rigidity | 49,512 multiset-breaking tests (R3) | **UNBREAKABLE** |
| Main conjecture η(C_p^4) = 17(p-1)+1 | All approaches | **UNCONTRADICTED** |

---

## WHAT IS PROVABLY DEAD

| Approach | Obstruction | Status |
|----------|-------------|--------|
| 1. Fiber induction (multi-fiber) | 3/2 gap; cap geometric obstruction | **DEAD** |
| 2. CW / Polynomial method | Can't encode integer weight | **DEAD** |
| 3. Character sum averaging (support ≥ 4) | Average = level for even k | **DEAD** |
| 4. Fiber + Sumset bootstrapping | Cross-fiber weight arithmetic | **DEAD** (same as 1 + metric mismatch) |
| 5. Extremal uniqueness | 4 GL classes at p=5 | **DEAD** |
| Previously dead: U1, U2, k=4 parity, cross-fiber collinear | See Sessions 1-4 | **STILL DEAD** |

---

## CRITICAL NEW FINDING: The n_1 = n_3 Symmetry Theorem

**Theorem (proved)**: For a 4-element dependency (a,b,c,d) ∈ (F_p*)^4 with a+b+c+d ≡ 0 (mod p), let n_k = |{μ ∈ F_p* : f_4(μ) = kp}| for k = 1, 2, 3. Then **n_1 = n_3**.

**Proof**: n_1 + n_2 + n_3 = p-1. And n_1·p + n_2·2p + n_3·3p = 2p(p-1) (from the average). Dividing: n_1 + 2n_2 + 3n_3 = 2(p-1). Subtracting: n_2 + 2n_3 = p-1. So n_3 = (p-1-n_2)/2 and n_1 = (p-1-n_2)/2 = n_3. □

**Corollary**: For a Case-0 dependency (coefficient sum ≡ 0 mod p), **exactly one** of the following holds:
- f_4(μ) ≡ 2p for all μ (i.e., n_1 = n_3 = 0), which happens iff the dependency is **paired**: {a,b,c,d} = {α, p-α, β, p-β} for some partition into pairs
- n_1 = n_3 ≥ 1, so **there EXISTS μ with f_4(μ) = p**, giving a zero-sum of weight exactly p ≤ p ✓

**What "paired" means geometrically**: The dependency α(v_1 - v_2) + β(v_3 - v_4) = 0 forces v_1 - v_2 ∝ v_3 - v_4. The four vectors form a **parallelogram**: two pairs share the same "direction of displacement."

**This reduces the character sum obstruction to a precise structural question**: Among 18 non-proportional vectors in F_p^4, can ALL Case-0 4-element dependencies be parallelograms?

If not — if even ONE non-paired Case-0 dependency exists — the n_1 = n_3 theorem gives weight p.

### Direction A: Killing the all-parallelogram hypothesis

The question: can 18 non-proportional vectors in F_p^{r+1} have the property that EVERY linearly dependent 4-tuple with coefficient-sum ≡ 0 (mod p) is a parallelogram?

**Constraint from parallelogram structure**: If {v_1, v_2, v_3, v_4} is a parallelogram (v_1-v_2 ∝ v_3-v_4), then the "difference directions" form a highly structured set. For n vectors, there are C(n,2) difference directions. The parallelogram condition forces: whenever 4 vectors are coplanar with Case-0 dependency, two difference directions must be proportional.

**At p=5, rank 4**: The 94 residual cases were killed by UNIT coefficient zero-sums (all s_i = 1, weight 4). A unit zero-sum v_i+v_j+v_k+v_l = 0 has dependency (1,1,1,1), which has coefficient sum 4 ≡ 4 ≠ 0 mod 5. This is a **Case ≠ 0** dependency! So the Case-0 analysis (and the parallelogram obstruction) doesn't even apply here.

**This means the p=5 killing mechanism is orthogonal to the parallelogram obstruction.** At p=5, the zero-sums use unit coefficients with weight 4 < p, not scaled Case-0 dependencies.

**The key question for larger p**: At p=7, weight ≤ 7. Unit zero-sums (weight 4) still work. But Case-0 dependencies with weight 7 also work — and the n_1=n_3 theorem handles all non-paired ones. The only remaining worry is: dependencies with coefficient sum ≢ 0 mod p AND no unit-coefficient zero-sum. But these have f_4(μ) ≡ μc mod p with c ≠ 0, and the integer value might exceed p for all μ.

**Bottom line**: The character sum approach works for:
- Support 3: always (rank-3 theorem, when non-degenerate)
- Support 4 + Case 0 + non-paired: always (n_1 = n_3 theorem)
- Support 4 + Case 0 + paired (parallelogram): NEVER (f_4 ≡ 2p)
- Support 4 + Case ≠ 0: SOMETIMES (depends on integer value, not just residue)

The proof must handle the remaining cases by other means (unit zero-sums, higher support, or structural arguments).

### Direction B: Expansion / additive combinatorics

If the set of 17 vectors generates F_p^4 (which it must, since 17 > 4), the sumsets Σ_w grow. The Plünnecke-Ruzsa inequality bounds sumset growth. If |Σ_1| = 17 and the doubling constant is small, |Σ_w| grows polynomially. But we need |Σ_{p-1}| = p^4 - 1 = 624 at p=5. With 17 generators and p-1=4 steps, can Plünnecke guarantee this?

The issue: Plünnecke gives |Σ_w| ≥ |Σ_1|^{w/1} / K^{w-1} for doubling constant K. At w=4, |Σ_4| ≥ 17^4/K^3. For this to reach 624: 17^4/K^3 ≥ 624, so K^3 ≤ 83521/624 ≈ 134, K ≤ 5.1. The doubling constant K = |Σ_2|/|Σ_1|. We need K ≤ 5.1. Since Σ_2 ⊂ F_5^4 and |Σ_2| ≤ 624, K ≤ 624/17 ≈ 36.7. This is way too large.

**Plünnecke is too weak.** The sumsets might grow fast enough empirically, but the general inequality doesn't force it.

### Direction C: Direct shadow saturation via linear algebra

Given 17 vectors spanning F_p^4, the set S generates F_p^4. The question: does Σ_{≤p-1}(S) = F_p^4 \ {0} follow from the ZSF condition alone?

This is equivalent to: the ZSF condition (no zero-sum of weight ≤ p) implies a COVERING condition (every nonzero vector is reachable with weight ≤ p-1). These feel dual. Is there a formal duality?

In coding theory: the minimum distance of the kernel code is ≥ p+1 (ZSF). The covering radius is what we need ≤ p-1 (shadow saturation). For MDS codes, covering radius = n-k and minimum distance = n-k+1. If our kernel code were MDS: d = n-k+1 = 14, not p+1 = 6. So the code is FAR from MDS.

**No known duality between minimum distance and covering radius gives what we need.**

---

## NEW ATTACK: The p=5 vs p=7 Boundary

At p=5, ALL killing zero-sums for the 94 residual cases use unit coefficients (all s_i = 1, weight 4). This is a very special mechanism. Let me examine whether it generalizes.

**Unit zero-sums**: v_{i₁} + v_{i₂} + v_{i₃} + v_{i₄} = 0 with weight 4 < p. This requires p > 4, i.e., p ≥ 5. ✓ for all primes in scope.

But: can we always FIND a 4-element unit zero-sum? This is a question about the additive structure of the vector set, not about rescaling.

**A 4-element unit zero-sum among n vectors** is a solution to v_i + v_j + v_k + v_l = 0. By the Cauchy-Davenport theorem and its generalizations, the sumset |A+B| ≥ min(p, |A|+|B|-1) over F_p. But we're working in F_p^4, not F_p, so Cauchy-Davenport doesn't directly apply.

**The cap connection**: A cap (no 3 collinear) in PG(3, F_p) can still have 4-element unit zero-sums: v_i + v_j + v_k + v_l = 0 doesn't require any 3 to be collinear. In fact, Claude-018 found that ALL zero-sums in concrete caps at p=5 are support-4 with weight 5 (= p, not 4).

Wait — weight 5, not 4? Let me re-read: "all 113 discovered zero-sums in concrete cap are support-4, weight 5." Weight 5 = p. These are NOT unit-coefficient zero-sums (weight 4); they're weight-p zero-sums with non-unit coefficients.

So for caps, the killing mechanism is different from the doubled+e₁ case. Caps use weighted (non-unit) zero-sums of weight exactly p.

**Implication**: The p=5 mechanism isn't just "find unit zero-sums." It's context-dependent:
- For doubled+e₁ + 18th vector: unit zero-sums (weight 4) suffice
- For cap configurations: weighted zero-sums (weight p) needed

This makes the proof harder — no single mechanism covers all cases.

**At p=7**: With the doubled+e₁ construction, 4-element unit zero-sums still have weight 4 < 7. But the number of candidate 18th vectors grows (F_7^4 has more projective points), and the fraction killed by support-3 (rank-3 subroutine) grows too (77% non-degenerate vs 44% at p=5). The residual cases needing support-4 should be FEWER.

**The boundary**: The proof difficulty peaks at p=5 (smallest prime, most degenerate triples, fewest unit zero-sums). If a proof works at p=5, it likely works at all larger p. This suggests p=5 should be the "base case" for the upper bound, with larger p being easier.

---

## VERDICT

All five proposed approaches to the multi-fiber upper bound have precise, named obstructions:

| # | Approach | Obstruction | Salvageable? |
|---|----------|-------------|--------------|
| 1 | Fiber induction | Permanent 3/2 gap, cap geometry | NO |
| 2 | CW / Polynomial | Can't encode integer weight | NO |
| 3 | Character sums | Average = level for even support | PARTIALLY (n_1=n_3 handles non-paired Case-0) |
| 4 | Fiber + Sumset | Reduces to #1 + metric mismatch | NO |
| 5 | Extremal uniqueness | 4 GL classes at p=5 | NO |

**The most promising directions**:

1. **The n_1 = n_3 theorem + all-parallelogram elimination**: Prove that ZSF 18-element sets must contain a non-paired Case-0 4-tuple. Then the character sum approach gives weight p. This requires a structural lemma about the "difference geometry" of ZSF sets.

2. **Unit zero-sum forcing**: Prove that among 18 non-proportional vectors in F_p^4, there always exist 4 that sum to zero (unit coefficients). This is a purely additive-combinatorial question, independent of the η machinery. At p=5, this is verified for all 607 residual cases.

3. **Direct shadow saturation**: Prove Σ_{≤p-1}(S) = F_p^4 \ {0} for every ZSF 17-set S, by a technique not yet identified. The empirical evidence (624/624 across all GL classes) is overwhelming. The coding-theoretic path faces metric issues but might work for p ≥ 7 where the L1/Hamming gap is less severe.

The empirical evidence strongly suggests the theorem is TRUE. The difficulty is entirely in the proof method. The problem needs a genuinely new idea — possibly combining the partial reach of the character sum approach (n_1 = n_3 for non-paired) with a structural argument eliminating the all-paired / all-parallelogram case.
