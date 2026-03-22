# Research Archive: η(C_p^r) Project

Complete archive of the research program proving η(C_p³) = 8(p−1)+1
and pursuing the all-ranks generalization ("the Grail").

Archived: 2026-03-21

## What's Here

### `/cortex/`
- `autonomous.db` — SQLite database with 529 entries from the multi-agent research cortex. Contains all discoveries, dead ends, conjectures, and proof fragments from the autonomous agent runs.
- `dual-server.py` — The MCP server code that runs both personal and autonomous cortex instances.

### `/proofs/`
- `gap_hypothesis_proof.md` — Complete analytical proof that Σ_{p-1}(A₈)^c = {(0,j,j) : 1 ≤ j ≤ (p-3)/2}. Five explicit constructions covering all off-L targets.
- `adversary_session5_round1.md` — The adversary agent's definitive report on why all five approaches to the multi-fiber upper bound fail. Contains the n₁=n₃ Symmetry Theorem.

### `/grail-tasks/`
- `cc-collab-v2.sh` — The collab orchestration system (theorist/computer/adversary, 3 rounds).
- `goal.md` — The current goal definition for agent runs.
- `*.md` — 39 research reports from various agent sessions.
- `collab-runs/` — 11 complete multi-round collab runs with all agent outputs and thinking traces.

### `/multi-agent/`
- `multi-agent.py` — The multi-agent research system (102KB). Supports claude/gpt/gemini/team architectures.
- `seeds/` — Seed briefings for agent runs.
- `team-runs/` — 194 agent briefs, results, and postmortems from team runs.

## What's Proved (as of archival)

| Theorem | Status |
|---------|--------|
| η(C_p³) = 8(p−1)+1, all odd primes p | **PROVED**, Lean-verified |
| η(C_p^r) ≥ (9·2^{r−3}−1)(p−1)+1, all r≥3 | **PROVED** (doubling+e₁) |
| s(C_p^r) = η(C_p^r) + p − 1 | **PROVED** (translation trick) |
| Gap Hypothesis (Σ_{p-1} gap is exactly L) | **PROVED** (5 constructions) |
| n₁=n₃ Symmetry Theorem (support-4 deps) | **PROVED** |
| η(C_p^r) ≤ (9·2^{r−3}−1)(p−1)+1, all r≥3 | **OPEN** (the Grail) |

## The Grail

Prove the **upper bound** η(C_p^r) ≤ (9·2^{r−3}−1)(p−1)+1 for all r≥3, all odd primes p.

The lower bound is proved. Proving the upper bound gives the **exact value** of η(C_p^r) for all elementary p-groups.

All systematic approaches have named obstructions (see adversary_session5_round1.md). The most promising leads at archival:
1. Weight Range Lemma (polytope dimension argument)
2. Parallelogram elimination + n₁=n₃ theorem
3. EGZ-within-EGZ (zero-sum nesting/refinement)

## Infrastructure

- **Cortex MCP servers**: Port 8080 (personal), Port 8082 (autonomous). Token: emc2ymmv.
- **Collab system**: `bash cc-collab-v2.sh <rounds> <goal.md>`. Needs Claude Code CLI.
- **Lean**: v4.14.0 with Mathlib. AWS EC2 for builds.
- **GitHub**: github.com/requitefahrenheit/davenport-eta-cp3
