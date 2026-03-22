#!/bin/bash
# Launch multiple Claude Code instances on grail research tasks
# Each runs on Max subscription (free)

cd ~/claude/grail-tasks
CLAUDE="$HOME/.npm-global/bin/claude"
export PATH=/opt/node20/bin:$PATH

echo "$(date): Launching grail research tasks..."

# Task 1: CW Congruence System
nohup $CLAUDE -p "$(cat task1-cw-congruences.md)" --output-format text \
  > results-cw-congruences.txt 2>&1 &
echo "Task 1 (CW congruences): PID $!"
sleep 2

# Task 2: Weighted CW (Grynkiewicz)
nohup $CLAUDE -p "$(cat task2-weighted-cw.md)" --output-format text \
  > results-weighted-cw.txt 2>&1 &
echo "Task 2 (weighted CW): PID $!"
sleep 2

# Task 3: Sumset Structure
nohup $CLAUDE -p "$(cat task3-sumset-structure.md)" --output-format text \
  > results-sumset.txt 2>&1 &
echo "Task 3 (sumset structure): PID $!"
sleep 2

# Task 4: Fiber Geometry
nohup $CLAUDE -p "$(cat task4-fiber-geometry.md)" --output-format text \
  > results-fiber-geometry.txt 2>&1 &
echo "Task 4 (fiber geometry): PID $!"
sleep 2

# Task 5: p=7 Exhaustive Verification
nohup $CLAUDE -p "$(cat task5-p7-exhaustive.md)" --output-format text \
  > results-p7-exhaustive.txt 2>&1 &
echo "Task 5 (p=7 exhaustive): PID $!"
sleep 2

# Task 6: Direct Proof Attempt
nohup $CLAUDE -p "$(cat task6-proof-attempt.md)" --output-format text \
  > results-proof-attempt.txt 2>&1 &
echo "Task 6 (proof attempt): PID $!"
sleep 2

# Task 7: Zero-Sum Decomposition
nohup $CLAUDE -p "$(cat task7-decomposition.md)" --output-format text \
  > results-decomposition.txt 2>&1 &
echo "Task 7 (decomposition): PID $!"

echo ""
echo "$(date): All 7 tasks launched."
echo "Monitor: ps aux | grep claude | grep -v grep"
echo "Results: ls -la ~/claude/grail-tasks/results-*.txt"
echo "Check: wc -l ~/claude/grail-tasks/results-*.txt"
