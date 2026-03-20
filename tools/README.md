# Autonomous Research Tools

Infrastructure for autonomous mathematical research using LLM agents.
Developed during the pursuit of η(C_p^r) bounds.

## tools/multi-agent/

**multi-agent.py** — Autonomous research agent with dual backend support.
- Architectures: Claude API, GPT, Gemini
- Worker/evaluator/narrator design (COMMIT/REFRAME/CHALLENGE/ABORT)
- Sandboxed Python computation
- Cortex integration for persistent cross-run memory
- Thinking extraction, rescue, and cross-pollination
- Post-mortem analysis on every exit
- Usage: `python multi-agent.py --prove goal.txt --seed seed.md --arch claude`

## tools/cc-collab/

**cc-collab-v2.sh** — Collaborative Claude Code research system.
Three Opus agents (theorist/computer/adversary) running in parallel on Max subscription.
- Haiku synthesis between rounds
- Thinking cross-pollination (extracts near-misses from each agent's thinking)
- Escalation protocol (2/3 agree → HIGH CONFIDENCE, 2/3 fail same → POSSIBLE FALSE)
- Adaptive role assignment (detect drift, swap roles)
- Connected to Cortex via MCP for shared memory
- Usage: `bash cc-collab-v2.sh 3 goal.md > /tmp/collab.log 2>&1`

**Supporting scripts:**
- `cc-wrapper.sh` — Single-agent wrapper with thinking capture
- `haiku_call.py` — Generic Haiku API caller (file-based, shell-safe)
- `extract_thinking.py` — Extract thinking blocks from stream-json output
- `final_summary.py` — Generate post-session summary via Haiku
- `parse_stream.py` — Parse Claude Code stream-json output
- `show_cortex.py` — Display recent Cortex entries
- `cortex-mcp.json` — MCP config connecting to autonomous Cortex
- `goal.md` — Current research goal (Shadow Saturation)

## Cortex Architecture

Two separate instances:
- **Personal** (port 8080): Jeremy's memory, used in conversations
- **Autonomous** (port 8082): Agent workspace, shared between research agents

## Key Lessons

See `handoff-2026-03-19.md` in the repo root for 14 rules of thumb
learned from building and operating this system.
