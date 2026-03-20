#!/bin/bash
# cc-collab-v2.sh — Collaborative Claude Code research system (v2)
#
# v2 additions:
#   1. Thinking cross-pollination: Haiku extracts near-misses from thinking,
#      feeds them to other agents next round
#   2. Escalation protocol: 2/3 agree → high-confidence; 2/3 fail same point → flag false
#   3. Adaptive role assignment: detect role drift, swap agents if needed
#
# Usage: bash cc-collab-v2.sh <rounds> <goal-file>

set -e

ROUNDS=${1:-3}
GOAL_FILE=${2:-goal.md}
DIR="$HOME/claude/grail-tasks"
CLAUDE="$HOME/.npm-global/bin/claude"
PYTHON="$HOME/miniforge3/bin/python3"
export PATH=/opt/node20/bin:$PATH
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000

SESSION="collab-$(date +%Y%m%d-%H%M%S)"
WORKDIR="$DIR/$SESSION"
mkdir -p "$WORKDIR"

GOAL=$(cat "$DIR/$GOAL_FILE")
MCP_CFG="$DIR/cortex-mcp.json"

# Agent definitions
AGENTS=("theorist" "computer" "adversary")

# Role prompts (can be swapped by adaptive assignment)
ROLE_theorist="You are the THEORIST. Your job is to prove theorems. Formulate lemmas, construct proofs, identify obstructions. You do NOT write code — state claims as [VERIFY: ...] for the computer to check. When you get findings from other agents, use them as building blocks. Store proved results to Cortex (mcp__claude_ai_autonomous__cortex_store). Search Cortex first (cortex_semantic_search) to avoid repeating dead ends. You MAY use web search to look up specific theorems, check if results exist in the literature, or find techniques from related problems. Cite what you find."

ROLE_computer="You are the COMPUTER. Your job is to verify conjectures, run exhaustive checks, compute examples, and find counterexamples. When the theorist states [VERIFY: ...], check it. When the adversary proposes a construction, test it. Write Python code for everything — no hand calculations. Store computational findings to Cortex. Search Cortex first to see what's been computed. You MAY use web search to find algorithms, lookup known constants or sequences (OEIS), or check computational results against published tables."

ROLE_adversary="You are the ADVERSARY. Your job is to break things. Try to construct counterexamples. When the theorist proposes a lemma, try to disprove it. When the computer verifies something at p=5, check if it fails at p=7 or p=11. Find the exact boundary where things break. Store counterexamples and near-misses to Cortex. Search Cortex first to see what others have found. You MAY use web search to find known counterexamples in the literature, lookup related conjectures that turned out false, or find constructions from other authors that might apply."

# Track current role assignment (for adaptive swapping)
ASSIGN_theorist="theorist"
ASSIGN_computer="computer"
ASSIGN_adversary="adversary"

# =====================================================================
# Function: run one agent for one round
# =====================================================================
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
    
    # Parse thinking, text, AND tool calls (full conversation)
    $PYTHON - <<'PYEOF' "$RAWFILE" "$OUTFILE.txt" "$THINKFILE"
import sys, json
raw_file, text_file, think_file = sys.argv[1:4]
thinking, conversation = [], []
with open(raw_file) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            if d.get('type') == 'assistant':
                for block in d.get('message',{}).get('content',[]):
                    bt = block.get('type','')
                    if bt == 'thinking':
                        thinking.append(block.get('thinking',''))
                    elif bt == 'text':
                        txt = block.get('text','')
                        if txt.strip():
                            conversation.append(txt)
                    elif bt == 'tool_use':
                        name = block.get('name','')
                        inp = block.get('input',{})
                        # Capture tool inputs (code, file paths, queries)
                        if name == 'Bash':
                            cmd = inp.get('command','')
                            conversation.append(f'\n[BASH] {cmd[:500]}\n')
                        elif name == 'Read':
                            conversation.append(f'[READ: {inp.get("file_path","")}]')
                        elif name == 'Write':
                            conversation.append(f'[WRITE: {inp.get("file_path","")}]')
                        elif 'cortex_store' in name:
                            content = inp.get('params',inp).get('content',inp.get('content',''))[:300]
                            conversation.append(f'\n[CORTEX STORE] {content}\n')
                        elif 'cortex_semantic' in name or 'cortex_search' in name:
                            q = inp.get('params',inp).get('query',inp.get('query',''))
                            conversation.append(f'[CORTEX SEARCH: {q}]')
                        else:
                            conversation.append(f'[TOOL: {name}]')
            elif d.get('type') == 'tool_result':
                # Capture tool output summaries
                content = d.get('content','')
                if isinstance(content, list):
                    content = ' '.join(c.get('text','') for c in content if isinstance(c,dict))[:500]
                elif isinstance(content, str):
                    content = content[:500]
                if content:
                    conversation.append(f'  -> {content[:500]}')
        except: pass
with open(text_file,'w') as f: f.write('\n'.join(conversation))
with open(think_file,'w') as f:
    for i,t in enumerate(thinking):
        f.write(f'\n{"="*60}\nBLOCK {i+1} ({len(t)} chars)\n{"="*60}\n{t}\n')
total_text = sum(len(c) for c in conversation)
total_think = sum(len(t) for t in thinking)
print(f"  [{text_file.split('/')[-1]}] {len(conversation)} entries ({total_text} chars), {len(thinking)} thinking ({total_think} chars)")
PYEOF
    
    echo "  [${AGENT}] Round ${ROUND} done."
}

# =====================================================================
# Feature 1: Thinking cross-pollination
# Extract near-misses from each agent's thinking, feed to others
# =====================================================================
extract_thinking_insights() {
    local ROUND=$1
    echo "  [CROSS] Extracting thinking insights from round ${ROUND}..."
    
    local SYS_TMP="$WORKDIR/.tmp_sys"
    echo 'Extract 2-3 key insights from this mathematician internal thinking that the OTHER agents should know about. Focus on: (1) Near-misses: proofs that almost worked and why they failed. (2) Structural observations that other approaches could use. (3) Unexpected connections or patterns noticed. Be terse. Each insight 1-2 sentences. State mathematical content precisely.' > "$SYS_TMP"
    
    for AGENT in "${AGENTS[@]}"; do
        local THINKFILE="$WORKDIR/${AGENT}-round${ROUND}-thinking.txt"
        local INSIGHTFILE="$WORKDIR/${AGENT}-round${ROUND}-insights.txt"
        
        if [ ! -f "$THINKFILE" ] || [ $(wc -c < "$THINKFILE") -lt 200 ]; then
            echo "" > "$INSIGHTFILE"
            continue
        fi
        
        head -c 8000 "$THINKFILE" > "$WORKDIR/.tmp_content"
        $PYTHON "$DIR/haiku_call.py" "$SYS_TMP" "$WORKDIR/.tmp_content" 600 > "$INSIGHTFILE" 2>/dev/null || echo "(extraction failed)" > "$INSIGHTFILE"
        echo "  [CROSS] ${AGENT}: $(wc -c < "$INSIGHTFILE") chars of insights extracted"
    done
    rm -f "$SYS_TMP" "$WORKDIR/.tmp_content"
}

# =====================================================================
# Feature 2: Escalation protocol
# Detect convergence or shared failure across agents
# =====================================================================
escalation_check() {
    local ROUND=$1
    echo "  [ESCAL] Running escalation check for round ${ROUND}..."
    
    # Collect all visible text
    local ALL=""
    for AGENT in "${AGENTS[@]}"; do
        local AFILE="$WORKDIR/${AGENT}-round${ROUND}.txt"
        if [ -f "$AFILE" ]; then
            ALL+="\n=== ${AGENT} ===\n$(head -c 3000 "$AFILE")\n"
        fi
    done
    
    # Haiku checks for convergence or shared failure
    echo 'You check for convergence and divergence among three researchers. Analyze their outputs and report: CONVERGENCE: If 2+ agents independently arrived at the same claim, state it and mark [HIGH CONFIDENCE]. SHARED FAILURE: If 2+ agents hit the same obstruction, state it and mark [POSSIBLE FALSE CONJECTURE]. CONTRADICTION: If agents disagree, state both sides and mark [NEEDS RESOLUTION]. If none apply, say NONE. Be precise.' > "$WORKDIR/.tmp_escal_sys"
    echo "$ALL" > "$WORKDIR/.tmp_escal_content"
    local ESCAL=$($PYTHON "$DIR/haiku_call.py" "$WORKDIR/.tmp_escal_sys" "$WORKDIR/.tmp_escal_content" 800 2>/dev/null || echo 'NONE')
    rm -f "$WORKDIR/.tmp_escal_sys" "$WORKDIR/.tmp_escal_content"
    
    echo "$ESCAL" > "$WORKDIR/escalation-round${ROUND}.txt"
    
    # Store escalations to Cortex if substantive
    if echo "$ESCAL" | grep -q 'HIGH CONFIDENCE\|POSSIBLE FALSE\|NEEDS RESOLUTION'; then
        curl -s -X POST "http://127.0.0.1:8082/mcp?token=emc2ymmv" \
            -H 'Content-Type: application/json' \
            -H 'Accept: application/json, text/event-stream' \
            -d "$(printf '%s' "{\"jsonrpc\":\"2.0\",\"id\":\"escal\",\"method\":\"tools/call\",\"params\":{\"name\":\"cortex_store\",\"arguments\":{\"content\":$(echo "$ESCAL" | head -c 2000 | $PYTHON -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"tags\":[\"auto\",\"escalation\",\"round${ROUND}\"],\"source\":\"cc-collab escalation, round ${ROUND}\"}}}" 2>/dev/null)" > /dev/null 2>&1
        echo "  [ESCAL] Escalation stored to Cortex"
    fi
    
    echo "  [ESCAL] $ESCAL" | head -5
    echo "$ESCAL"
}

# =====================================================================
# Feature 3: Adaptive role assignment
# Detect role drift, swap agents if needed
# =====================================================================
adaptive_roles() {
    local ROUND=$1
    echo "  [ADAPT] Checking role alignment for round ${ROUND}..."
    
    local ALL=""
    for AGENT in "${AGENTS[@]}"; do
        local AFILE="$WORKDIR/${AGENT}-round${ROUND}.txt"
        if [ -f "$AFILE" ]; then
            ALL+="\n=== ${AGENT} (assigned: ${AGENT}) ===\n$(head -c 2000 "$AFILE")\n"
        fi
    done
    
    echo "Three researchers have roles: THEORIST (proves theorems, no code), COMPUTER (writes code, verifies), ADVERSARY (finds counterexamples). Check if each stayed in role. If drifted, say SWAP agent1 agent2. If OK, say ROLES OK. Say which was MOST PRODUCTIVE." > "$WORKDIR/.tmp_adapt_sys"
    echo "$ALL" > "$WORKDIR/.tmp_adapt_content"
    local ADAPT=$($PYTHON "$DIR/haiku_call.py" "$WORKDIR/.tmp_adapt_sys" "$WORKDIR/.tmp_adapt_content" 400 2>/dev/null || echo "ROLES OK")
    rm -f "$WORKDIR/.tmp_adapt_sys" "$WORKDIR/.tmp_adapt_content"
    
    echo "$ADAPT" > "$WORKDIR/adaptive-round${ROUND}.txt"
    echo "  [ADAPT] $ADAPT" | head -3
    
    # Parse swap directives
    if echo "$ADAPT" | grep -q '^SWAP'; then
        local A1=$(echo "$ADAPT" | grep '^SWAP' | head -1 | awk '{print $2}')
        local A2=$(echo "$ADAPT" | grep '^SWAP' | head -1 | awk '{print $3}')
        if [ -n "$A1" ] && [ -n "$A2" ]; then
            echo "  [ADAPT] SWAPPING roles: $A1 <-> $A2"
            # Swap the role prompts
            local TEMP_VAR="ROLE_${A1}"
            local TEMP_VAL="${!TEMP_VAR}"
            local OTHER_VAR="ROLE_${A2}"
            eval "ROLE_${A1}=\"${!OTHER_VAR}\""
            eval "ROLE_${A2}=\"${TEMP_VAL}\""
            eval "ASSIGN_${A1}=${A2}"
            eval "ASSIGN_${A2}=${A1}"
        fi
    fi
}

# =====================================================================
# Coordinator synthesis (enhanced with cross-pollination + escalation)
# =====================================================================
synthesize() {
    local ROUND=$1
    echo "  [COORD] Synthesizing round ${ROUND}..."
    
    # Step 1: Extract thinking insights (Feature 1)
    extract_thinking_insights "$ROUND"
    
    # Step 2: Escalation check (Feature 2)
    local ESCAL_RESULT=$(escalation_check "$ROUND")
    
    # Step 3: Adaptive role check (Feature 3)
    adaptive_roles "$ROUND"
    
    # Step 4: Collect all agent outputs + insights
    local ALL_TEXT=""
    for AGENT in "${AGENTS[@]}"; do
        local AFILE="$WORKDIR/${AGENT}-round${ROUND}.txt"
        local IFILE="$WORKDIR/${AGENT}-round${ROUND}-insights.txt"
        if [ -f "$AFILE" ]; then
            local CONTENT=$(head -c 3000 "$AFILE")
            ALL_TEXT+="\n=== ${AGENT^^} OUTPUT ===\n${CONTENT}\n"
        fi
    done
    
    # Add cross-pollination insights for OTHER agents
    local CROSS_INSIGHTS=""
    for AGENT in "${AGENTS[@]}"; do
        local IFILE="$WORKDIR/${AGENT}-round${ROUND}-insights.txt"
        if [ -f "$IFILE" ] && [ -s "$IFILE" ]; then
            CROSS_INSIGHTS+="\nInsights from ${AGENT}'s thinking:\n$(cat "$IFILE")\n"
        fi
    done
    
    # Add escalation results
    local ESCAL_FILE="$WORKDIR/escalation-round${ROUND}.txt"
    local ESCAL_TEXT=""
    if [ -f "$ESCAL_FILE" ]; then
        ESCAL_TEXT=$(cat "$ESCAL_FILE")
    fi
    
    # Haiku main synthesis
    echo "You coordinate three mathematical researchers: THEORIST, COMPUTER, ADVERSARY. Produce a synthesis with: ## STATUS (one sentence), ## CONVERGENCE/ESCALATION (HIGH CONFIDENCE or POSSIBLE FALSE CONJECTURE flags), ## CROSS-POLLINATION (insights from thinking), ## DIRECTIVES (one instruction per agent, referencing other agents findings, creating dependencies)." > "$WORKDIR/.tmp_synth_sys"
    printf "%s\n\n%s\n\n%s" "$ALL_TEXT" "$CROSS_INSIGHTS" "$ESCAL_TEXT" > "$WORKDIR/.tmp_synth_content"
    local SYNTHESIS=$($PYTHON "$DIR/haiku_call.py" "$WORKDIR/.tmp_synth_sys" "$WORKDIR/.tmp_synth_content" 2500 2>/dev/null || echo "Synthesis failed")
    rm -f "$WORKDIR/.tmp_synth_sys" "$WORKDIR/.tmp_synth_content"
    
    echo "$SYNTHESIS" > "$WORKDIR/synthesis-round${ROUND}.txt"
    echo "  [COORD] Synthesis written to synthesis-round${ROUND}.txt"
    
    # Store synthesis to Cortex
    curl -s -X POST "http://127.0.0.1:8082/mcp?token=emc2ymmv" \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -d "$(printf '%s' "{\"jsonrpc\":\"2.0\",\"id\":\"coord\",\"method\":\"tools/call\",\"params\":{\"name\":\"cortex_store\",\"arguments\":{\"content\":$(echo "$SYNTHESIS" | head -c 2000 | $PYTHON -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"tags\":[\"auto\",\"synthesis\",\"round${ROUND}\",\"v2\"],\"source\":\"cc-collab-v2 coordinator, round ${ROUND}\"}}}" 2>/dev/null)" > /dev/null 2>&1
    
    echo "$SYNTHESIS"
}

# =====================================================================
# MAIN LOOP
# =====================================================================

echo "$(date): cc-collab-v2 starting. Session: $SESSION"
echo "  Goal: $(head -1 $DIR/$GOAL_FILE)"
echo "  Rounds: $ROUNDS"
echo "  Agents: ${AGENTS[*]}"
echo "  Features: thinking-cross-pollination, escalation, adaptive-roles"
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
    
    # Get current role assignments
    local_theorist_role="ROLE_${ASSIGN_theorist}"
    local_computer_role="ROLE_${ASSIGN_computer}"
    local_adversary_role="ROLE_${ASSIGN_adversary}"
    
    # Build context block
    CONTEXT="RESEARCH GOAL:\n$GOAL\n"
    if [ $ROUND -eq 1 ]; then
        CONTEXT+="\nSEED DOCUMENT (prior research):\n$SEED\n"
        CONTEXT+="\nPOST-MORTEM (prior agent run):\n$POSTMORTEM\n"
    fi
    if [ -s "$WORKDIR/synthesis-round$((ROUND-1)).txt" ] 2>/dev/null; then
        CONTEXT+="\n=== COORDINATOR SYNTHESIS FROM LAST ROUND ===\n"
        CONTEXT+=$(cat "$WORKDIR/synthesis-round$((ROUND-1)).txt" | tr '\`' "'" | tr '$' 'S')
        CONTEXT+="\n=== END SYNTHESIS ===\n"
    fi
    
    # Add cross-pollination insights from previous round (Feature 1)
    # Write per-agent cross files (no eval, no shell injection)
    for AGENT in "${AGENTS[@]}"; do
        echo "" > "$WORKDIR/.cross-${AGENT}.txt"
    done
    if [ $ROUND -gt 1 ]; then
        PREV=$((ROUND - 1))
        for AGENT in "${AGENTS[@]}"; do
            for OTHER in "${AGENTS[@]}"; do
                if [ "$OTHER" != "$AGENT" ]; then
                    OFILE="$WORKDIR/${OTHER}-round${PREV}-insights.txt"
                    if [ -f "$OFILE" ] && [ -s "$OFILE" ]; then
                        echo "From ${OTHER}'s reasoning last round:" >> "$WORKDIR/.cross-${AGENT}.txt"
                        cat "$OFILE" >> "$WORKDIR/.cross-${AGENT}.txt"
                        echo "" >> "$WORKDIR/.cross-${AGENT}.txt"
                    fi
                fi
            done
        done
    fi
    
    CONTEXT+="\nRound $ROUND of $ROUNDS. Make it count.\n"
    
    # Read cross-pollination from files (safe from shell injection)
    THEORIST_CROSS=$(cat "$WORKDIR/.cross-theorist.txt" 2>/dev/null | tr '\`' "'" | tr '$' 'S')
    COMPUTER_CROSS=$(cat "$WORKDIR/.cross-computer.txt" 2>/dev/null | tr '\`' "'" | tr '$' 'S')
    ADVERSARY_CROSS=$(cat "$WORKDIR/.cross-adversary.txt" 2>/dev/null | tr '\`' "'" | tr '$' 'S')
    
    THEORIST_PROMPT="${!local_theorist_role}\n\n${CONTEXT}"
    if [ -n "$THEORIST_CROSS" ]; then
        THEORIST_PROMPT+="\n=== INSIGHTS FROM OTHER AGENTS' THINKING ===\n${THEORIST_CROSS}\n=== END INSIGHTS ===\n"
    fi
    THEORIST_PROMPT+="\nSearch Cortex first. Read ~/claude/multi-agent/seeds/grail-briefing.md if round 1. Prove something new."
    
    COMPUTER_PROMPT="${!local_computer_role}\n\n${CONTEXT}"
    if [ -n "$COMPUTER_CROSS" ]; then
        COMPUTER_PROMPT+="\n=== INSIGHTS FROM OTHER AGENTS' THINKING ===\n${COMPUTER_CROSS}\n=== END INSIGHTS ===\n"
    fi
    COMPUTER_PROMPT+="\nSearch Cortex first. Read ~/claude/multi-agent/seeds/grail-briefing.md if round 1. Compute something definitive."
    
    ADVERSARY_PROMPT="${!local_adversary_role}\n\n${CONTEXT}"
    if [ -n "$ADVERSARY_CROSS" ]; then
        ADVERSARY_PROMPT+="\n=== INSIGHTS FROM OTHER AGENTS' THINKING ===\n${ADVERSARY_CROSS}\n=== END INSIGHTS ===\n"
    fi
    ADVERSARY_PROMPT+="\nSearch Cortex first. Read ~/claude/multi-agent/seeds/grail-briefing.md if round 1. Break something or prove it unbreakable."
    
    # Run agents in parallel
    run_agent "theorist" "$ROUND" "$THEORIST_PROMPT" &
    PID_T=$!
    run_agent "computer" "$ROUND" "$COMPUTER_PROMPT" &
    PID_C=$!
    run_agent "adversary" "$ROUND" "$ADVERSARY_PROMPT" &
    PID_A=$!
    
    echo "  Agents running: theorist=$PID_T computer=$PID_C adversary=$PID_A"
    echo "  Role assignments: theorist=${ASSIGN_theorist} computer=${ASSIGN_computer} adversary=${ASSIGN_adversary}"
    
    # Wait for all agents
    wait $PID_T $PID_C $PID_A
    echo "  All agents done for round $ROUND."
    
    # Synthesize (includes cross-pollination, escalation, adaptive roles)
    synthesize "$ROUND"
    
    # Read synthesis from file, strip shell-hostile characters (backticks, $)
    PREV_SYNTHESIS=$(cat "$WORKDIR/synthesis-round${ROUND}.txt" 2>/dev/null | tr '\`' "'" | tr '$' 'S' || echo "")
    
    # Clear cross-pollination vars for next round
    CROSS_theorist=""
    CROSS_computer=""
    CROSS_adversary=""
    
    echo ""
    echo "--- SYNTHESIS (round $ROUND) ---"
    cat "$WORKDIR/synthesis-round${ROUND}.txt" 2>/dev/null
    echo "--- END SYNTHESIS ---"
    echo ""
done

# =====================================================================
# Final session summary
# =====================================================================
echo "======================================"
echo "SESSION COMPLETE: $SESSION"
echo "======================================"

# Generate final post-mortem across all rounds
$PYTHON "$DIR/final_summary.py" "$WORKDIR" "$ROUNDS" > "$WORKDIR/final-summary.txt" 2>/dev/null || echo "Final summary failed" > "$WORKDIR/final-summary.txt"

echo "  Final summary written to $WORKDIR/final-summary.txt"
cat "$WORKDIR/final-summary.txt"

echo ""
echo "Workdir: $WORKDIR"
echo "Files:"
ls -la "$WORKDIR"/*.txt 2>/dev/null | awk '{print "  " $NF ": " $5 " bytes"}'
