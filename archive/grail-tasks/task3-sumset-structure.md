# Task: Sumset Structure of ZSF Sets in F_p^3

Read ~/claude/multi-agent/seeds/grail-briefing.md for context.

## The Question

Let A be a zero-sum-free (ZSF) set of 8 nonzero non-proportional vectors in F_p^3. This means: no coefficients s_1,...,s_k in {1,...,p-1} with sum(s_i) <= p and sum(s_i * a_i) = 0.

Equivalently: in the multiset where each a_i appears p-1 times, there is no subsequence of length <= p summing to zero.

The key construction is A8 = {e1, e2, e3, -e1+e2+e3, e1+e2, e1+e3, -e1+2e2+e3, -e1+e2+2e3} in F_5^3.

## Computational Tasks

1. For A8 at p=5: compute |A8 + A8|, |A8 + A8 + A8|, |A8 + A8 + A8 + A8| (iterated sumsets). Report exact sizes and what fraction of F_5^3 = 125 they cover.

2. For A8 at p=5: compute the SIGNED sumset {a - b : a, b in A8, a != b}. How large is it? Does it cover all of F_5^3 \ {0}?

3. The 94 failure cases in the grail verification need 4-element zero-sums v1+v2+v3+v4=0 (weight 4 < p=5). This means v4 is in -(v1+v2+v3) = the 3-fold sumset -3A. Compute: for how many elements x in F_5^3 is x in the 3-fold sumset {a+b+c : a,b,c distinct elements of A8}?

4. Generalize: for a RANDOM 8-element non-proportional set B in F_p^3 (p=5,7,11), compute the same sumset sizes. Compare with A8. Is A8 extremal (smallest sumsets)?

5. Compute the ADDITIVE ENERGY E(A8) = |{(a,b,c,d) in A8^4 : a+b=c+d}|. High additive energy means additive structure; low energy means pseudo-random. What does A8 look like?

6. The Pluennecke-Ruzsa inequality says: if |A+A| <= K|A|, then |kA| <= K^k |A|. For A8: what is K = |A8+A8|/|A8|? What does this predict for |3A8|, |4A8|? Does the prediction match the actual values?

7. KEY QUESTION: For a general ZSF set A of size n in F_p^r, is there a lower bound on |A+A| that comes from the ZSF property? The ZSF condition says 0 is not in Sigma_<=p(A^{p-1}). Does this force |A+A| to be large?

8. Freiman's theorem: if |A+A| <= K|A|, then A is contained in a generalized arithmetic progression of dimension d and size f(K)|A|. For A8: what GAP contains it? Does the ZSF property constrain which GAPs are possible?

Save results to ~/claude/grail-tasks/results-sumset.txt
