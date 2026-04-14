"""
重新生成 520 四象限 HTML
X 轴改为：搜索爆发系数 = 大促搜索UV日均 / 基期搜索UV日均
大促期：20250519-20250520（2天）
基期：20250512-20250518（7天）
"""
import json, re, math, csv
from collections import defaultdict, OrderedDict

# ── 1. 读取原始数据 ──
raw_content = open('/Users/lisicong/Desktop/kancong-daily/520_raw_result.json').read()
idx = raw_content.find('[')
raw = json.loads(raw_content[idx:])

PROMO_DAYS = ['20250519', '20250520']
BASE_DAYS  = ['20250512','20250513','20250514','20250515','20250516','20250517','20250518']

# ── 2. 按三级品类聚合 ──
agg = defaultdict(lambda: {
    'promo_ss_uv': 0, 'base_ss_uv': 0,
    'promo_gmv': 0.0, 'base_gmv': 0.0,
    'promo_feishi_gmv': 0.0,
    'l1': '', 'l2': ''
})

for row in raw:
    dt  = row['dt']
    key = (row['prod_first_category_name'],
           row['prod_second_category_name'],
           row['prod_third_category_name'])
    d = agg[key]
    d['l1'] = row['prod_first_category_name']
    d['l2'] = row['prod_second_category_name']
    ss_uv       = int(row['ss_view_uv'] or 0)
    gmv         = float(row['actual_total_price'] or 0)
    feishi_gmv  = float(row['feishi_actual_total_price'] or 0)

    if dt in PROMO_DAYS:
        d['promo_ss_uv']      += ss_uv
        d['promo_gmv']        += gmv
        d['promo_feishi_gmv'] += feishi_gmv
    elif dt in BASE_DAYS:
        d['base_ss_uv'] += ss_uv
        d['base_gmv']   += gmv

# ── 3. 读取基期搜索UV（补跑的 CSV）──
base_ss_csv = {}
csv_path = '/Users/lisicong/Desktop/kancong-daily/base_ss_uv.csv/bi_query_336584173.csv'
with open(csv_path) as f:
    for row in csv.DictReader(f):
        k = (row['prod_first_category_name'],
             row['prod_second_category_name'],
             row['prod_third_category_name'])
        base_ss_csv[k] = float(row['base_ss_view_uv_total'])

# ── 4. 计算指标 ──
MIN_FEISHI_GMV = 100000  # 大促非食GMV ≥ 10万

points = []
for key, d in agg.items():
    l1, l2, l3 = key
    promo_feishi_gmv = d['promo_feishi_gmv']
    if promo_feishi_gmv < MIN_FEISHI_GMV:
        continue

    # 搜索爆发系数 = 大促搜索UV日均 / 基期搜索UV日均
    promo_ss_avg = d['promo_ss_uv'] / len(PROMO_DAYS)
    base_ss_total = base_ss_csv.get(key, d['base_ss_uv'])
    base_ss_avg   = base_ss_total / len(BASE_DAYS)
    if base_ss_avg <= 0:
        continue
    ss_burst = promo_ss_avg / base_ss_avg

    # GTV爆发系数（大促日均 / 基期日均，用总GMV）
    base_gmv_avg  = d['base_gmv'] / len(BASE_DAYS)
    promo_gmv_avg = d['promo_gmv'] / len(PROMO_DAYS)
    if base_gmv_avg <= 0:
        continue
    gtv_burst = promo_gmv_avg / base_gmv_avg

    points.append({
        'l1': l1, 'l2': l2, 'name': l3,
        'x': round(ss_burst, 4),
        'y': round(gtv_burst, 4),
        'gmv': round(promo_feishi_gmv),
        'promo_ss_uv': round(promo_ss_avg),
        'base_ss_uv':  round(base_ss_avg),
    })

print(f"有效品类数: {len(points)}")

# ── 5. P70 分界线 ──
xs = sorted([p['x'] for p in points])
ys = sorted([p['y'] for p in points])
x_p70 = round(xs[int(len(xs)*0.70)], 4)
y_p70 = round(ys[int(len(ys)*0.70)], 4)
print(f"X P70 (搜索爆发系数): {x_p70}")
print(f"Y P70 (GTV爆发系数):  {y_p70}")

# ── 6. 气泡大小 ──
gmv_vals = [p['gmv'] for p in points]
gmv_min, gmv_max = min(gmv_vals), max(gmv_vals)
def bubble_size(gmv):
    ratio = (math.log10(gmv+1) - math.log10(gmv_min+1)) / (math.log10(gmv_max+1) - math.log10(gmv_min+1))
    return round(10 + ratio * 45, 1)
for p in points:
    p['symbolSize'] = bubble_size(p['gmv'])

# ── 7. 按一级品类分组 ──
groups = OrderedDict()
for p in points:
    groups.setdefault(p['l1'], []).append(p)

# ── 8. ECharts series ──
COLORS = [
    '#5470c6','#91cc75','#fac858','#ee6666','#73c0de',
    '#3ba272','#fc8452','#9a60b4','#ea7ccc','#d14a61',
    '#675bba','#f05b72','#ef5b9c','#f47920','#0065bd',
    '#c0c0c0','#7fb80e','#00a0e9','#a6a6a6','#e60012',
]
series_data = []
for i, (l1, pts) in enumerate(groups.items()):
    data = []
    for p in pts:
        data.append({
            'value': [p['x'], p['y'], p['gmv']],
            'name': p['name'],
            'l2': p['l2'],
            'symbolSize': p['symbolSize'],
            'promo_ss_uv': p['promo_ss_uv'],
            'base_ss_uv':  p['base_ss_uv'],
        })
    series_data.append({'name': l1, 'type': 'scatter', 'data': data, 'color': COLORS[i % len(COLORS)]})

# ── 9. 象限统计 ──
q1 = [p for p in points if p['x'] >= x_p70 and p['y'] >= y_p70]
q2 = [p for p in points if p['x'] >= x_p70 and p['y'] <  y_p70]
q3 = [p for p in points if p['x'] <  x_p70 and p['y'] >= y_p70]
q4 = [p for p in points if p['x'] <  x_p70 and p['y'] <  y_p70]
for label, q in [('Q1双强爆发',q1),('Q2搜索领先',q2),('Q3GTV领先',q3),('Q4基础保障',q4)]:
    print(f"{label}: {len(q)}个, GMV={sum(p['gmv'] for p in q)/1e4:.0f}万")

result = {
    'series': series_data,
    'x_p70': x_p70, 'y_p70': y_p70,
    'total': len(points),
    'q_counts': [len(q1), len(q2), len(q3), len(q4)],
    'q_gmvs':   [sum(p['gmv'] for p in q)/1e4 for q in [q1,q2,q3,q4]],
}
json.dump(result, open('/tmp/quadrant_data_v2.json','w'), ensure_ascii=False)
print("数据已保存到 /tmp/quadrant_data_v2.json")
