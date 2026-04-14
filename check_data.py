import json
from collections import Counter

with open('520_raw_result.json') as f:
    content = f.read()

start = content.find('[')
end = content.rfind(']') + 1
data = json.loads(content[start:end])
print('Total rows:', len(data))

dt_counts = Counter(d['dt'] for d in data)
for dt in sorted(dt_counts):
    print(f'  {dt}: {dt_counts[dt]} rows')
