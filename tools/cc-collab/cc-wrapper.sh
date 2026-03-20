#!/bin/bash
# Claude Code wrapper that captures thinking blocks and saves to file
# Usage: ./cc-wrapper.sh <task-name> <prompt-file>

TASK_NAME="$1"
PROMPT_FILE="$2"
OUTPUT_DIR="$HOME/claude/grail-tasks"
CLAUDE="$HOME/.npm-global/bin/claude"
export PATH=/opt/node20/bin:$PATH
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000

TEXT_FILE="$OUTPUT_DIR/results-${TASK_NAME}.txt"
THINK_FILE="$OUTPUT_DIR/thinking-${TASK_NAME}.txt"
RAW_FILE="$OUTPUT_DIR/raw-${TASK_NAME}.json"

PROMPT=$(cat "$PROMPT_FILE")

echo "$(date): Starting task $TASK_NAME (opus, effort=max, cortex connected)" >> "$OUTPUT_DIR/launch.log"

# Run Claude Code with opus, max effort, stream-json, cortex MCP
$CLAUDE -p "$PROMPT" \
  --model opus \
  --effort max \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions \
  --mcp-config "$OUTPUT_DIR/cortex-mcp.json" \
  2>/dev/null > "$RAW_FILE"

echo "$(date): Task $TASK_NAME finished" >> "$OUTPUT_DIR/launch.log"

# Parse: extract thinking and text blocks
$HOME/miniforge3/bin/python3 - <<'PYEOF' "$RAW_FILE" "$TEXT_FILE" "$THINK_FILE" "$TASK_NAME"
import sys, json

raw_file, text_file, think_file, task_name = sys.argv[1:5]

thinking_blocks = []
text_blocks = []

with open(raw_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            if d.get('type') == 'assistant':
                msg = d.get('message', {})
                for block in msg.get('content', []):
                    btype = block.get('type', '')
                    if btype == 'thinking':
                        thinking_blocks.append(block.get('thinking', ''))
                    elif btype == 'text':
                        text_blocks.append(block.get('text', ''))
                    elif btype == 'tool_use':
                        text_blocks.append(f"[TOOL: {block.get('name', '?')}({json.dumps(block.get('input', {}))[:200]})]")
                    elif btype == 'tool_result':
                        content = block.get('content', '')
                        if isinstance(content, list):
                            content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
                        text_blocks.append(f"[RESULT: {str(content)[:500]}]")
        except:
            pass

with open(text_file, 'w') as f:
    f.write('\n'.join(text_blocks))

with open(think_file, 'w') as f:
    for i, t in enumerate(thinking_blocks):
        f.write(f'\n{"="*70}\nTHINKING BLOCK {i+1} ({len(t)} chars)\n{"="*70}\n')
        f.write(t + '\n')

print(f'{task_name}: {len(text_blocks)} text blocks ({sum(len(t) for t in text_blocks)} chars), '
      f'{len(thinking_blocks)} thinking blocks ({sum(len(t) for t in thinking_blocks)} chars)')
PYEOF
