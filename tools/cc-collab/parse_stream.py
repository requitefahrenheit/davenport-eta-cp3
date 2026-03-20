import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        if d.get('type') == 'assistant':
            msg = d.get('message', {})
            for block in msg.get('content', []):
                btype = block.get('type', '?')
                if btype == 'thinking':
                    text = block.get('thinking', '')
                    print(f'  THINKING block: {len(text)} chars')
                    print(f'    Preview: {text[:200]}')
                elif btype == 'text':
                    text = block.get('text', '')
                    print(f'  TEXT block: {len(text)} chars')
                    print(f'    Preview: {text[:200]}')
                else:
                    print(f'  {btype} block')
    except:
        pass
