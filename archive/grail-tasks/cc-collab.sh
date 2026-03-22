#!/bin/bash
# cc-collab.sh — Collaborative Claude Code research system
#
# Three Opus agents + Haiku coordinator, sharing Cortex memory.
# Runs in rounds: agents work in parallel, coordinator synthesizes,
# agents get each other's findings for next round.
#
# Usage: bash cc-collab.sh <rounds> <goal-file>
#   e.g.: bash cc-collab.sh 3 goal.md

set -e

ROUNDS=${1:-3}
GOAL_FILE=${2:-goal.md}
DIR="$HOME/claude/grail-tasks"
CLAUDE="$HOME/.npm-global/bin/claude"
PYTHON="$HOME/miniforge3/bin/python3"
export PATH=/opt/node20/bin:$PATH

SESSION="collab-$(date +%Y%m%d-%H%M%S)"
WORKDIR="$DIR/$SESSION"
mkdir -p "$WORKDIR"

GOAL=$(cat "$DIR/$GOAL_FILE")
MCP_CFG="$DIR/cortex-mcp.json"

# Agent definitions: name, system prompt addendum
AGENTS=("theorist" "computer" "adversary")

THEORIST_ROLE="You are the THEORIST. Your job is to prove theorems. Formulate lemmas, construct proofs, identify obstructions. You do NOT write code — state claims as [VERIFY: ...] for the computer to check. When you get findings from other agents, use them as building blocks. Store proved results to Cortex (mcp__claude_ai_autonomous__cortex_store). Search Cortex first (cortex_semantic_search) to avoid repeating dead ends."

COMPUTER_ROLE="You are the COMPUTER. Your job is to verify conjectures, run exhaustive checks, compute examples, and find counterexamples. When the theorist states [VERIFY: ...], check it. When the adversary proposes a construction, test it. Write Python code for everything — no hand calculations. Store computational findings to Cortex. Search Cortex first to see what's been computed."

ADVERSARY_ROLE="You are the ADVERSARY. Your job is to break things. Try to construct counterexamples. When the theorist proposes a lemma, try to disprove it. When the computer verifies something at p=5, check if it fails at p=7 or p=11. Find the exact boundary where things break. Store counterexamples and near-misses to Cortex. Search Cortex first to see what others have found."

# Function: run one agent for one round
run_agent() {
    local AGENT=$1
    local ROUND=$2
    local PROMPT=$3
    local OUTFILE="$WORKDIR/${AGENT}-round${ROUND}"
    local RAWFILE="$WORKDIR/${AGENT}-round${ROUND}-raw.json"
    local THINKFILE="$WORKDIR/${AGENT}-round${ROUND}-thinking.txt"
    
    echo "  [${AGENT}] Starting round ${ROUND}..."
    
    $CLAUDE -p "$PROMPT" \
        --model opus \
        --effort max \
        --output-format stream-json \
        --verbose \
        --dangerously-skip-permissions \
        --mcp-config "$MCP_CFG" \
        2>/dev/null > "$RAWFILE"
    
    # Parse thinking and text
    $PYTHON - <<'PYEOF' "$RAWFILE" "$OUTFILE.txt" "$THINKFILE"
import sys, json
raw_file, text_file, think_file = sys.argv[1:4]
thinking, text = [], []
with open(raw_file) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            if d.get('type') == 'assistant':
                for block in d.get('message',{}).get('content',[]):
                    bt = block.get('type','')
                    if bt == 'thinking': thinking.append(block.get('thinking',''))
                    elif bt == 'text': text.append(block.get('text',''))
                    elif bt == 'tool_use': text.append(f"[TOOL: {block.get('name','')}]")
        except: pass
with open(text_file,'w') as f: f.write('\n'.join(text))
with open(think_file,'w') as f:
    for i,t in enumerate(thinking):
        f.write(f'\n{"="*60}\nBLOCK {i+1} ({len(t)} chars)\n{"="*60}\n{t}\n')
print(f"  [{sys.argv[1].split('/')[-1].replace('-raw.json','')}] {len(text)} text, {len(thinking)} thinking ({sum(len(t) for t in thinking)} chars)")
PYEOF
    
    echo "  [${AGENT}] Round ${ROUND} done."
}

# Function: coordinator synthesis
synthesize() {
    local ROUND=$1
    echo "  [COORD] Synthesizing round ${ROUND}..."
    
    # Collect all agent outputs from this round
    local ALL_TEXT=""
    for AGENT in "${AGENTS[@]}"; do
        local AFILE="$WORKDIR/${AGENT}-round${ROUND}.txt"
        if [ -f "$AFILE" ]; then
            local CONTENT=$(head -c 4000 "$AFILE")
            ALL_TEXT+="\n=== ${AGENT^^} (round ${ROUND}) ===\n${CONTENT}\n"
        fi
    done
    
    # Also pull recent Cortex entries
    local CORTEX_RECENT=$(curl -s "http://127.0.0.1:8082/api/list?limit=5&token=emc2ymmv" 2>/dev/null | $PYTHON -c '
import sys, json
try:
    d = json.load(sys.stdin)
    for e in d.get("entries",[])[:5]:
        print(f"[{e.get(\"tags\",[])}] {e[\"content\"][:200]}")
except: pass
' 2>/dev/null)
    
    # Haiku synthesizes
    local SYNTHESIS=$($PYTHON - <<PYEOF
import os, json
from anthropic import Anthropic
client = Anthropic()
all_text = """$ALL_TEXT"""
cortex = """$CORTEX_RECENT"""

resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2000,
    system=(
        "You coordinate three mathematical researchers: THEORIST (proves theorems), "
        "COMPUTER (verifies computations), ADVERSARY (finds counterexamples). "
        "Summarize what each found this round. Identify: (1) agreements, (2) conflicts, "
        "(3) what each agent should focus on next round. Flag any claimed proofs that "
        "need verification. Flag any dead ends being revisited. Be concrete and terse. "
        "End with a DIRECTIVE for each agent: one sentence each."
    ),
    messages=[{"role":"user","content":f"Round ${ROUND} outputs:\n{all_text}\n\nRecent Cortex entries:\n{cortex}"}]
)
print(resp.content[0].text)
PYEOF
)
    
    echo "$SYNTHESIS" > "$WORKDIR/synthesis-round${ROUND}.txt"
    echo "  [COORD] Synthesis written to synthesis-round${ROUND}.txt"
    
    # Store synthesis to Cortex
    curl -s -X POST "http://127.0.0.1:8082/mcp?token=emc2ymmv" \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -d "$(printf '%s' "{\"jsonrpc\":\"2.0\",\"id\":\"coord\",\"method\":\"tools/call\",\"params\":{\"name\":\"cortex_store\",\"arguments\":{\"content\":$(echo "$SYNTHESIS" | head -c 2000 | $PYTHON -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"tags\":[\"auto\",\"synthesis\",\"round${ROUND}\"],\"source\":\"cc-collab coordinator, round ${ROUND}\"}}}" 2>/dev/null)" > /dev/null 2>&1
    
    # Return synthesis for injection
    echo "$SYNTHESIS"
}

# =====================================================================
# MAIN LOOP
# =====================================================================

echo "$(date): cc-collab starting. Session: $SESSION"
echo "  Goal: $(head -1 $DIR/$GOAL_FILE)"
echo "  Rounds: $ROUNDS"
echo "  Agents: ${AGENTS[*]}"
echo "  Workdir: $WORKDIR"
echo ""

# Read seed files
SEED=""
if [ -f "$HOME/claude/multi-agent/seeds/grail-briefing.md" ]; then
    SEED=$(head -c 6000 "$HOME/claude/multi-agent/seeds/grail-briefing.md")
fi
POSTMORTEM=""
if [ -f "$HOME/claude/multi-agent/claude-023-postmortem" ]; then
    POSTMORTEM=$(head -c 3000 "$HOME/claude/multi-agent/claude-023-postmortem")
fi

PREV_SYNTHESIS=""

for ROUND in $(seq 1 $ROUNDS); do
    echo "======================================"
    echo "ROUND $ROUND / $ROUNDS"
    echo "======================================"
    
    # Build agent prompts
    CONTEXT="RESEARCH GOAL:\n$GOAL\n"
    if [ $ROUND -eq 1 ]; then
        CONTEXT+="\nSEED DOCUMENT (prior research):\n$SEED\n"
        CONTEXT+="\nPOST-MORTEM (prior agent run):\n$POSTMORTEM\n"
    fi
    if [ -n "$PREV_SYNTHESIS" ]; then
        CONTEXT+="\n=== COORDINATOR SYNTHESIS FROM LAST ROUND ===\n$PREV_SYNTHESIS\n=== END SYNTHESIS ===\n"
    fi
    CONTEXT+="\nRound $ROUND of $ROUNDS. Make it count.\n"
    
    THEORIST_PROMPT="${THEORIST_ROLE}\n\n${CONTEXT}\n\nSearch Cortex first for prior findings. Read ~/claude/multi-agent/seeds/grail-briefing.md if this is round 1. Prove something new this round."
    COMPUTER_PROMPT="${COMPUTER_ROLE}\n\n${CONTEXT}\n\nSearch Cortex first for claims needing verification. Read ~/claude/multi-agent/seeds/grail-briefing.md if this is round 1. Compute something definitive this round."
    ADVERSARY_PROMPT="${ADVERSARY_ROLE}\n\n${CONTEXT}\n\nSearch Cortex first for claimed results to attack. Read ~/claude/multi-agent/seeds/grail-briefing.md if this is round 1. Break something or prove it unbreakable this round."
    
    # Run agents in parallel
    run_agent "theorist" "$ROUND" "$THEORIST_PROMPT" &
    PID_T=$!
    run_agent "computer" "$ROUND" "$COMPUTER_PROMPT" &
    PID_C=$!
    run_agent "adversary" "$ROUND" "$ADVERSARY_PROMPT" &
    PID_A=$!
    
    echo "  Agents running: theorist=$PID_T computer=$PID_C adversary=$PID_A"
    
    # Wait for all agents
    wait $PID_T $PID_C $PID_A
    echo "  All agents done for round $ROUND."
    
    # Synthesize
    PREV_SYNTHESIS=$(synthesize "$ROUND")
    
    echo ""
    echo "--- SYNTHESIS (round $ROUND) ---"
    echo "$PREV_SYNTHESIS"
    echo "--- END SYNTHESIS ---"
    echo ""
done

# Final summary
echo "======================================"
echo "SESSION COMPLETE: $SESSION"
echo "======================================"
echo "Workdir: $WORKDIR"
echo "Files:"
ls -la "$WORKDIR"/*.txt 2>/dev/null | awk '{print "  " $NF ": " $5 " bytes"}'
echo ""
echo "To review:"
echo "  cat $WORKDIR/synthesis-round*.txt"
echo "  cat $WORKDIR/theorist-round*.txt"
echo "  cat $WORKDIR/computer-round*.txt"
echo "  cat $WORKDIR/adversary-round*.txt"
echo "  # Thinking (the gold):"
echo "  cat $WORKDIR/*-thinking.txt"
