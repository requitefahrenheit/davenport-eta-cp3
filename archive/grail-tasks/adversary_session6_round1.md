# Adversary Report — Session 6 Round 1 (2026-03-21)

## Summary

Attacked every active claim in the grail proof. The shadow saturation chain is **sound**. The SINGLE remaining gap is **uniqueness of doubled+e1**. Found one new obstruction (support-4 weight fixed point) and confirmed the uniqueness gap is real and hard.

---

## Finding 1: Support-4 Weight Obstruction (NEW)

**The dependency (1,2,3,4) in F_5 produces weight 2p for ALL rescalings mu.**

Proof: {1,2,3,4} = F_5*, so rescaling by mu permutes the terms, preserving sum = 10 = 2p.

More generally: any k-element dependency with **antipodal coefficient pairs** {a, p-a} gives constant weight kp/2.

| k | Weight options (sum=0 mod p) | mu<->(p-mu) pairing | Can weight p be avoided? |
|---|------------------------------|---------------------|--------------------------|
| 3 | {p, 2p}                      | p <-> 2p            | NO: exactly (p-1)/2 mu give weight p |
| 4 | {p, 2p, 3p}                  | p <-> 3p, 2p fixed  | YES: all weights can be 2p |
| 5 | {p, 2p, 3p, 4p}              | p <-> 4p, 2p <-> 3p | YES: all weights can be 2p or 3p |

**Proof for k=3 (weight p always achieved):**
N1 + N2 = p-1 and p*N1 + 2p*N2 = 3p(p-1)/2. Solution: N1 = N2 = (p-1)/2.

**Concrete examples at p=5 where weight p is blocked (k=4):**
- (1,2,3,4): weight 10 for all mu (full residue system)
- (1,1,4,4) = {1,-1,1,-1}: weight 10 for all mu (antipodal pairs)
- (2,2,2,4): weight NOT constant (mu=1 -> 10, mu=2 -> 15), so this structure is specific

**Implication:** Support-4+ zero-sums cannot be guaranteed from individual linear dependencies. Any proof must use **global structure** across multiple dependencies. The 94 residual cases at p=5 use UNWEIGHTED 4-sums (all coefficients 1), sidestepping this obstruction.

---

## Finding 2: Uniqueness Gap -- Confirmed Real and Hard

The grail reduces to: doubled+e1 is the unique strongly ZSF set of size 2*alpha(r)+1.

### Logic chain verified (no circularity)

1. eta(C_p^3) = 8(p-1)+1 [PROVED, Lean-verified]
2. Shadow sat at rank 3: Sigma_{p-1}(A) = F_p^3 \ {0} for any maximal ZSF 8-set [PROVED from eta]
3. Shadow sat lifts to doubled+e1 in F_p^4 [PROVED, Theorem 2]
4. Projection strategy: any v18 added to S17 creates zero-sum [PROVED from shadow sat]
5. IF S17 is unique ZSF 17-set, then any 18 directions have a zero-sum [NEEDS UNIQUENESS]

Step 5 logic: given 18 directions, consider all C(18,17)=18 subsets of size 17. If none ZSF, each has internal zero-sum -> done. If one IS ZSF, uniqueness says it's S17, and step 4 handles the 18th.

### Attack attempts on uniqueness

**Attempt 1**: Replace coefficient 2 with 3 in A8.
B8 = {..., (4,3,1), (4,1,3)} at p=5. BREAKS ZSF: (1,1,0)+(1,0,1)+(4,3,1)+(4,1,3) = (0,0,0), weight 4.

**Attempt 2**: GL-equivalent constructions (scaling e1 -> 2e1). Same orbit, not genuine alternative.

**Structural observation**: coefficient 2 satisfies 2^2 = -1 mod 5. At p=13, 5^2 = -1. The role of sqrt(-1) in A8 may be algebraically essential, suggesting uniqueness depends on quadratic residue structure.

### Why uniqueness is hard to prove

1. No theoretical tool exists for proving uniqueness of maximal ZSF sets
2. Computational verification only at p=5,7 -- does not scale
3. Uniqueness at rank r does NOT obviously imply uniqueness at rank r+1
4. Multi-fiber alternatives (e.g. 6+6+5 across 3 fibers) not theoretically excluded

---

## Finding 3: What I Could NOT Break

1. **Shadow saturation proof** (Theorem 1): uses only eta definition + ZSF. Rock-solid.
2. **Two-fiber bound**: case analysis correct (eta bound on fiber 0, s bound on fiber c)
3. **Projection strategy**: valid when v_k = v18 (at most 1 projection becomes 0, leaves >= 16 nonzero)
4. **Lower bound construction**: doubled+e1 is ZSF at all p (structural, p-independent)
5. **s = eta + p - 1**: trivial, correct

---

## Finding 4: p=5 Is the Hardest Case

As p grows:
- Non-degenerate collinear triple fraction -> 1 (44% at p=5, 77% at p=13, ~100% as p -> inf)
- Weight bound p grows, making support-k zero-sums easier
- The support-4 weight-2p obstruction requires |F_p*| = k, which only holds at p=5 for k=4

Both effects make the conjecture easier at larger p.

---

## Finding 5: Cortex Inconsistency

The phase-2 Cortex entry (team-001-computer-brief) says "eta(C_p^3) = 8(p-1)+1 for p >= 7 | CONJECTURED, p=7 search suggests FALSE". This is WRONG -- the result is PROVED and Lean-verified for all p >= 5. The p=7 search found no random extremal supports, but that only means extremal configurations are rare/structured. Future agents should not be misled by this entry.

---

## Recommendations

The ONLY productive attack surface is **uniqueness**. Three approaches:

1. **Computational**: Verify uniqueness at p=11 (where sqrt(-1) does not exist, since 11 = 3 mod 4). If A8 needs sqrt(-1), a different extremal set might appear.

2. **Structural inverse theorem**: Prove any ZSF set of size 2*alpha(r)+1 must have <= 2 nonempty fibers under some projection. This would reduce uniqueness to the 2-fiber case, which is handled.

3. **Additive combinatorics**: Connect to sum-product estimates or Freiman-type inverse theorems. A maximal ZSF set is a very constrained additive structure; inverse theorems might force it into the doubled+e1 form.
