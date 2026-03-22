You are a mathematician working on a hard open problem. You have Cortex memory (mcp__claude_ai_autonomous__cortex_store and cortex_semantic_search). You can run Python. You can read files.

READ FIRST (use Read tool):
- ~/claude/multi-agent/seeds/grail-briefing.md  
- ~/claude/multi-agent/claude-023-postmortem

THE PROBLEM: Among 18 nonzero non-proportional vectors in F_p^4, prove a weighted zero-sum of weight <= p exists.

YOUR SPECIFIC ANGLE: The zero-sum decomposition strategy.

Here is what's known:
- D(C_p^4) = 4(p-1)+1. The copies pool (17 vectors, each with mult p-1, size 17(p-1)) is massive.
- By Grynkiewicz Theorem 1.8 with d=4, p>=7: s_{kp}(C_p^4) <= kp + 4p - 4 for k >= 4.
- So a zero-sum of length 4p exists in our pool. Weight 4p.
- We need weight p. The gap factor is 4.

YOUR TASK: Prove that any weight-4p zero-sum can be DECOMPOSED to contain a weight-p sub-zero-sum.

Approach A: Reiher cascading. If T is a zero-sum of length 3p, remove any element g. Then |T\g| = 3p-1. Apply CW to T\g: if N_{2p}(T\g) > 0, then T contains a length-2p zero-sum, whose complement in T is a length-p zero-sum. DONE.

Prove: for our specific sequence structure (17 distinct generators in C_p^4, each repeated p-1 times), N_{2p}(T\g) > 0 for any zero-sum T of length 3p and any g in T.

Approach B: Pigeonhole on fibers. A weight-4p zero-sum uses vectors from multiple fibers. The total weight 4p is distributed across fibers as W_0 + W_1 + ... = 4p with the fiber constraint sum(c * W_c) = 0 mod p. Can we always find a subset of fibers whose contribution has weight <= p and still sums to zero?

Approach C: The Davenport constant of the quotient. Project to a 1-dimensional quotient via a linear form. The weight-4p zero-sum projects to a weight-4p zero-sum in C_p. In C_p, D(C_p) = p. So the projected zero-sum can be partitioned into zero-sums in C_p, each of weight >= p. There are at most 4 such pieces. Lift back: at least one piece has weight p and maps to a weight-p zero-sum in the fiber.

Wait — does this work? The projection loses information. A zero-sum in the quotient isn't a zero-sum in the original unless the FIBER contribution is also zero. But the fiber contribution is in C_p^3...

Think through this carefully. Write Python code to test on explicit examples at p=5. State and prove lemmas. Store results to Cortex.
