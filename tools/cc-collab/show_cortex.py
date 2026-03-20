import json, sys
with open('/tmp/cortex_latest.json') as f:
    d = json.load(f)
print('Total entries:', d['total'])
for e in d['entries'][:10]:
    ts = e['timestamp'][11:19]
    tags = e.get('tags',[])
    pre = e['content'][:150].replace('\n',' ')
    print()
    print(f'  {ts} | {tags}')
    print(f'  {pre}')
