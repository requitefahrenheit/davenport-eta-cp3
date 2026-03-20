# Prove Shadow Saturation for ZSF Sets

Prove: for any zero-sum-free (ZSF) set S of 2α(r)+1 nonzero non-proportional vectors in F_p^{r+1} (p >= 5), the weight-(p-1) shadow covers all of F_p^{r+1} \ {0}.

That is: for every nonzero v in F_p^{r+1}, there exist vectors v_{i1},...,v_{ik} in S and coefficients c_1,...,c_k in {1,...,p-1} with c_1 + ... + c_k <= p-1 and c_1*v_{i1} + ... + c_k*v_{ik} = v.

Why this matters: if shadow saturation holds, then ANY 18th nonzero vector v is reachable at weight <= p-1. Adding coefficient p-1 on -v (or 1 on v with the shadow representation giving -v) produces a zero-sum of weight <= p. This proves eta(C_p^{r+1}) <= (2*alpha(r)+1)(p-1)+1 — the grail.

Computational evidence (from Agent 3, stored in Cortex):
- p=5: shadow of 17-vector ZSF set covers all 624 nonzero vectors at weight 4 = p-1. VERIFIED.
- p=7: shadow covers all 2400 nonzero vectors at weight 6 = p-1. VERIFIED.
- Random non-ZSF 17-vector sets NEVER achieve full coverage (even 20 vectors don't). Shadow saturation is ZSF-specific.
- All 17 vectors are critical — remove any one and the shadow develops gaps.

Key structural facts:
- ZSF means 0 is NOT in the shadow at any weight. All shadow capacity goes to nonzero targets.
- The copies pool (each vector with mult p-1) has |S|*(p-1) = (2α(r)+1)(p-1) elements.
- D*(C_p^{r+1}) = (r+1)(p-1)+1. For the base case r=3: D* = 4p-3.

Promising approaches:
1. CW/polynomial counting of shadow representations mod p
2. Sumset growth: |kS| grows until it covers F_p^{r+1}
3. Induction on weight: show each weight level adds enough new targets
4. Character-sum argument showing the shadow can't have gaps

Dead ends (DO NOT revisit):
- Character theory for support >= 4 (W(chi) = 0 for even characters)
- Classical CW degree argument (fires only for p=5)
- Grail Lemma (N_p(kp-ZS) ≡ k mod p) — FALSE for ZSF sequences
- Weight-4p → weight-p decomposition — FAILS

Search Cortex (autonomous instance) for prior findings. Read ~/claude/multi-agent/seeds/grail-briefing.md for full context.
