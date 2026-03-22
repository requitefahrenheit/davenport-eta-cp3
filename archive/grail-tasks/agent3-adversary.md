You are a mathematician working on a hard open problem. You have Cortex memory (mcp__claude_ai_autonomous__cortex_store and cortex_semantic_search). You can run Python. You can read files.

READ FIRST (use Read tool):
- ~/claude/multi-agent/seeds/grail-briefing.md
- ~/claude/multi-agent/claude-023-postmortem

THE PROBLEM: Among 18 nonzero non-proportional vectors in F_p^4, prove a weighted zero-sum of weight <= p exists.

YOUR SPECIFIC ANGLE: Play the ADVERSARY. Try to CONSTRUCT a counterexample.

If the theorem is true, you will fail — and the failure mode will reveal the proof.

Your task:

1. For p=5: try to construct 18 nonzero non-proportional vectors in F_5^4 with NO zero-sum of weight <= 5. Start with the doubled+e1 construction (which achieves 17). Try to extend it. You know all 607 extensions fail — but WHY do they fail? What property of the 17-vector set makes extension impossible?

2. For p=7: same exercise but with more room. Try to construct 18 vectors in F_7^4 with no weight-<=7 zero-sum. You have more freedom (p^4 = 2401 possible vectors vs 625 at p=5). Try systematically:
   a. Start with A8 in fiber 0 (8 vectors)
   b. Add A8 in fiber 1 (8 more vectors, total 16)
   c. Add e1 (total 17)
   d. Try to add an 18th vector that avoids ALL zero-sums of weight <= 7
   e. For each candidate, check support-3, support-4, support-5, support-6, support-7.

3. Try a COMPLETELY DIFFERENT base construction. Not doubled+e1. What if the fibers have sizes (7, 7, 4) instead of (8, 9, 1)? Or (6, 6, 6)? Does the fiber distribution matter?

4. The key structural question: what is the EXACT obstruction to extending from 17 to 18? Is it:
   a. Too many collinear triples (can't avoid them all)?
   b. The sumset coverage (A+A+A covers too much of F_p^3)?
   c. Some algebraic invariant (like the Davenport constant of a subgroup)?
   d. Something else entirely?

Formulate conjectures about WHAT MAKES EXTENSION IMPOSSIBLE. Test them. If you find a pattern, state it as a precise conjecture and attempt a proof.

5. The ultimate question: is there a POLYNOMIAL CERTIFICATE that proves a set of 17 vectors in F_p^4 cannot be extended? Something like: for any 17-vector ZSF set S, the polynomial P_S(x) = product over weight-<=p zero-sums vanishes on all of F_p^4. This would mean no extension exists.

Write code. Test examples. But always aim for STRUCTURE, not just data. Store insights to Cortex.
