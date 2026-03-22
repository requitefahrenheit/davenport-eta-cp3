# Task: Fiber Geometry and Collinear Triple Avoidance

Read ~/claude/multi-agent/seeds/grail-briefing.md for context.

## The Question

The grail proof reduces (after the two-fiber bound) to: among 18 nonzero non-proportional vectors in F_p^4 spanning >= 3 hyperplane fibers, must there exist either:
(a) A non-degenerate collinear triple (handled by rank-3 theorem), or
(b) A 4-element zero-sum of weight < p?

A key fact: cross-fiber collinear triples with fiber labels (0, 1, c) where c >= 2 are AUTOMATICALLY non-degenerate. So if such a triple exists, the rank-3 theorem fires.

The computational finding at p=5: 0 out of 94 failure cases have such cross-fiber collinear triples. But they all have 4-element zero-sums.

## Computational Tasks

1. For p=5: construct ALL possible configurations of 18 non-proportional nonzero vectors in F_5^4 that span exactly 3 fibers under w = first coordinate. Enumerate: how many such configurations avoid ALL non-degenerate collinear triples?

2. For p=7: same question. With 18 vectors spanning 3+ fibers in F_7^4, can we avoid all non-degenerate collinear triples? If yes, do those configurations always have 4-element zero-sums of weight < 7?

3. The incidence question: given sets B_0 (size a) and B_1 (size b) in F_p^3 (projections of fiber-0 and fiber-1 vectors), and a single point x in F_p^3 (projection of a fiber-c vector), when does x lie on a line through a point of B_0 and a point of B_1?

The line through b0 in B_0 and b1 in B_1 is {alpha*b0 + beta*b1 : (alpha:beta) in P^1}.
The point x lies on this line iff x = alpha*b0 + beta*b1 for some alpha, beta.

For EACH x in F_p^3: count how many (b0, b1) pairs have x on their line.
Total incidences = sum over x of count(b0, b1).
By double counting: total = |B_0| * |B_1| * (p-1) (each line has p-1 non-endpoint points).

4. If |B_0| = 8, |B_1| = 9 (our case): total incidences = 72(p-1). In F_p^3 with p^3 - 1 = 124 nonzero points (p=5): average incidences per point = 72*4/124 = 2.32. So most points are hit. But CAN all 18 points avoid being hit?

5. For p=7: total incidences = 72*6 = 432, ambient = 342. Average = 1.26. Lower coverage. For p=17: average = 72*16/4912 = 0.23. Most points NOT hit. So for large p, cross-fiber avoidance IS possible.

6. THE KEY: What ADDITIONAL structure does the ZSF (zero-sum-free) condition impose? If B_0 and B_1 are both ZSF in F_p^3, does that force MORE incidences between them?

Specifically: if B_0 is ZSF and b1 in B_1, then b1 cannot be in the sumset {s1*a + s2*b : a,b in B_0, s1+s2 <= p, s1*a+s2*b = b1}. Does this constrain where B_1 can sit relative to B_0?

7. EXPERIMENT: For p=5,7,11, generate 10000 random pairs (B_0, B_1) where both are ZSF sets of size 8 in F_p^3 (no proportional pairs, no zero-sum of weight <= p). For each pair, check if any point of B_1 lies on a line through two points of B_0. What fraction of random ZSF pairs have cross-fiber collinear triples?

Save results to ~/claude/grail-tasks/results-fiber-geometry.txt
