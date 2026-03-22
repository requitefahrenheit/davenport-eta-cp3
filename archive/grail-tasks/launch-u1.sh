#!/bin/bash
# Launch U1-focused collab run
export PATH=/opt/node20/bin:$HOME/.npm-global/bin:$PATH
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000
cd ~/claude/grail-tasks
bash cc-collab-v2.sh 3 goal.md > /tmp/cc-collab.log 2>&1
