#!/usr/bin/env python3
"""Generate final session summary from synthesis and escalation files.
Usage: python3 final_summary.py <workdir> <rounds>
"""
import sys, json, os
from anthropic import Anthropic

workdir = sys.argv[1]
rounds = int(sys.argv[2])

synths = []
for r in range(1, rounds + 1):
    path = os.path.join(workdir, f"synthesis-round{r}.txt")
    try:
        with open(path) as f:
            synths.append(f"Round {r}:\n{f.read()[:1500]}")
    except:
        pass

escals = []
for r in range(1, rounds + 1):
    path = os.path.join(workdir, f"escalation-round{r}.txt")
    try:
        with open(path) as f:
            content = f.read().strip()
            if content and content != 'NONE':
                escals.append(f"Round {r}: {content[:500]}")
    except:
        pass

all_input = "\n\n".join(synths)
if escals:
    all_input += "\n\nESCALATIONS:\n" + "\n".join(escals)

if not all_input.strip():
    print("No synthesis files found.")
    sys.exit(0)

client = Anthropic()
resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2000,
    system=(
        "Write a final research summary of a multi-round collaborative research session. "
        "State: (1) what was PROVED, (2) what was DISPROVED, (3) what remains OPEN, "
        "(4) the single most promising next step. Be precise with mathematical claims."
    ),
    messages=[{"role": "user", "content": all_input}]
)
print(resp.content[0].text)
