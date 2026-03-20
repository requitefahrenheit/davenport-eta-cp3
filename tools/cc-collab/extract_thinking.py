import json, sys

raw_file = sys.argv[1]
out_file = sys.argv[2]

thinking = []
with open(raw_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            if d.get('type') == 'assistant':
                for block in d.get('message', {}).get('content', []):
                    if block.get('type') == 'thinking':
                        thinking.append(block['thinking'])
        except:
            pass

with open(out_file, 'w') as f:
    for i, t in enumerate(thinking):
        sep = '=' * 60
        f.write(f'\n{sep}\nBLOCK {i+1} ({len(t)} chars)\n{sep}\n{t}\n')

print(f'Extracted {len(thinking)} blocks, {sum(len(t) for t in thinking)} chars total')
