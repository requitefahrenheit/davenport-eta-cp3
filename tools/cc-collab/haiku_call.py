#!/usr/bin/env python3
"""Generic Haiku caller. Reads system prompt and user content from files.
Usage: python3 haiku_call.py <system_file> <content_file> [max_tokens]
"""
import sys, json
from anthropic import Anthropic

system_file = sys.argv[1]
content_file = sys.argv[2]
max_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

with open(system_file) as f:
    system = f.read()
with open(content_file) as f:
    content = f.read()

client = Anthropic()
resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=max_tokens,
    system=system,
    messages=[{"role": "user", "content": content}]
)
print(resp.content[0].text)
