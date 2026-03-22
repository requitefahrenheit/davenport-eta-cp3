You are a mathematician of the caliber of Gauss, Euler, Erdos, Ramanujan. You have access to Cortex memory (use mcp__claude_ai_autonomous__cortex_store and mcp__claude_ai_autonomous__cortex_semantic_search). You can run Python code. You can read files.

READ THESE FILES FIRST (use the Read tool):
- ~/claude/multi-agent/seeds/grail-briefing.md
- ~/claude/multi-agent/claude-023-postmortem
- ~/claude/grail-tasks/results-cw-congruences.txt

THE PROBLEM: Prove eta(C_p^4) <= 17(p-1)+1 for all p >= 5.
Equivalently: among 18 nonzero non-proportional vectors in F_p^4, there exists a weighted zero-sum of weight <= p.

CRITICAL FINDING: CW congruences alone have 2-3 free variables. They DON'T force N_p > 0. The proof MUST use structural input from the rank-3 theorem.

Your job: FORMULATE AND PROVE CONJECTURES. Not compute. Not survey. PROVE.

Here is your attack plan:

1. The rank-3 theorem says: for any non-degenerate collinear triple (a,b,c in F_p*, no pair summing to 0, sum != 0), there exists mu with <mu*a>+<mu*b>+<mu*c> < p. This FORCES certain N_j to be positive.

Quantify this: among 18 vectors in F_p^4, how many non-degenerate collinear triples exist? Each one contributes to N_p or N_{2p} or N_{3p}. This gives LOWER BOUNDS on specific N_j values.

Conjecture: the number of non-degenerate collinear triples among 18 generic vectors in F_p^4 is at least f(p) for some explicit function f.

2. Now combine: CW gives linear relations among N_j mod p. Rank-3 gives N_j >= g(p) for specific j. If g(p) > 0 and the CW relations force N_p = 0 to be incompatible with the lower bounds, we're done.

3. The adversary's view: to make N_p = 0, you need all weight-p zero-sums to cancel mod p in the CW system. But rank-3 forces many of them to exist. Can they all have weight exactly 2p or 3p, never p? Prove they can't.

Do actual math. Write lemmas. State claims precisely. Use computation only to verify claims, not to explore blindly. Store proved results to Cortex. If you get stuck, state PRECISELY what blocks you.

You have one shot. Make it count.
