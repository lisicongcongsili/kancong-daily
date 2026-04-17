import pandas as pd, json, os

df = pd.read_excel('520大促三级品类明细.xlsx', sheet_name='520大促', header=2)
df.columns = ['rank','cat1','cat2','cat3','promo_gtv','promo_gtv_w','promo_order','promo_order_w',
              'promo_nonfood_gtv','promo_nonfood_order','base_gtv','base_order',
              'base_nonfood_gtv','base_nonfood_order','base_search_uv','avg_price',
              'burst_gtv','burst_order','burst_nonfood_gtv','burst_nonfood_order','price_change']
df = df.dropna(subset=['cat3'])
for c in ['burst_gtv','burst_order','promo_gtv_w']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df2 = df.dropna(subset=['burst_gtv','burst_order','promo_gtv_w']).copy()
df2 = df2[(df2['burst_gtv']>0)&(df2['burst_order']>0)]

# X轴=闪购GTV爆发系数，Y轴=闪购订单爆发系数，气泡=大促GTV
XT = round(df2['burst_gtv'].quantile(0.7), 4)
YT = round(df2['burst_order'].quantile(0.7), 4)

MAX_SYM = 60.0; MIN_SYM = 5.0
gtv_min = df2['promo_gtv_w'].min(); gtv_max = df2['promo_gtv_w'].max()

def sym_size(v):
    ratio = (v - gtv_min) / (gtv_max - gtv_min) if gtv_max != gtv_min else 0
    return round(MIN_SYM + ratio * (MAX_SYM - MIN_SYM), 1)

colors = {
    '个人洗护':'#E63946','厨具餐具':'#457B9D','学习/办公用品':'#2A9D8F','宠物生活':'#E9C46A',
    '家居日用':'#F4A261','家庭清洁':'#6D6875','家用电器':'#A8DADC','家纺布艺':'#264653',
    '家装建材':'#B5838D','彩妆香水':'#FFAFCC','成人用品':'#BDE0FE','手机通讯':'#CDB4DB',
    '服饰鞋包':'#80B918','母婴用品':'#FF6B6B','玩具乐器':'#4ECDC4','珠宝首饰':'#45B7D1',
    '电脑数码':'#96CEB4','美容护肤':'#F6BD60','节庆礼品':'#DDA0DD','运动户外':'#98D8C8'
}

# 过滤异常点（其他黄金配饰 x=30.8, y=25.1）
OUTLIERS = ['其他黄金配饰', '铂金']

series_map = {}
for _, row in df2.iterrows():
    c1 = row['cat1']; c3 = row['cat3']
    if c3 in OUTLIERS:
        continue
    x = round(float(row['burst_gtv']), 4)
    y = round(float(row['burst_order']), 4)
    gtv = round(float(row['promo_gtv_w']), 1)
    sz = sym_size(float(row['promo_gtv_w']))
    if c1 not in series_map:
        series_map[c1] = {
            'name': c1, 'type': 'scatter', 'data': [],
            'itemStyle': {'color': colors.get(c1,'#999'), 'opacity': 0.82},
            'emphasis': {'itemStyle': {'opacity':1,'borderColor':'#fff','borderWidth':2},
                         'label': {'show':True,'formatter':'{b}','fontSize':12,'fontWeight':'bold','color':'#222'}},
            'label': {'show': False}
        }
    series_map[c1]['data'].append({'value':[x,y,gtv],'name':c3,'symbolSize':sz})

series = list(series_map.values())

df3 = df2[~df2['cat3'].isin(OUTLIERS)]
q1 = df3[(df3['burst_gtv']>=XT)&(df3['burst_order']>=YT)]
q2 = df3[(df3['burst_gtv']<XT)&(df3['burst_order']>=YT)]
q3 = df3[(df3['burst_gtv']>=XT)&(df3['burst_order']<YT)]
q4 = df3[(df3['burst_gtv']<XT)&(df3['burst_order']<YT)]

stats = {
    '双强':    {'count':len(q1),'gtv':round(q1['promo_gtv_w'].sum(),1),'top3':q1.nlargest(3,'promo_gtv_w')['cat3'].tolist()},
    '订单强':  {'count':len(q2),'gtv':round(q2['promo_gtv_w'].sum(),1),'top3':q2.nlargest(3,'promo_gtv_w')['cat3'].tolist()},
    'GTV强':   {'count':len(q3),'gtv':round(q3['promo_gtv_w'].sum(),1),'top3':q3.nlargest(3,'promo_gtv_w')['cat3'].tolist()},
    '稳健增长':{'count':len(q4),'gtv':round(q4['promo_gtv_w'].sum(),1),'top3':q4.nlargest(3,'promo_gtv_w')['cat3'].tolist()},
}

series_json = json.dumps(series, ensure_ascii=False)
stats_json  = json.dumps(stats,  ensure_ascii=False)
colors_json = json.dumps(colors, ensure_ascii=False)

print(f"XT={XT}, YT={YT}")
print(f"stats={stats_json}")

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>520大促 · 三级品类四象限分析</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',sans-serif;background:#F7F8FA;color:#1A1A1A}}
.wrap{{max-width:1280px;margin:0 auto;padding:20px 24px}}
.header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}}
.title{{font-size:18px;font-weight:700;color:#1A1A1A;letter-spacing:.5px}}
.subtitle{{font-size:12px;color:#888;margin-top:4px}}
.badge{{background:linear-gradient(135deg,#FF6B9D,#FF4081);color:#fff;font-size:11px;font-weight:600;padding:4px 10px;border-radius:12px;letter-spacing:.5px}}
.kpi-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}}
.kpi{{background:#fff;border-radius:10px;padding:14px 16px;border-left:4px solid #ddd;box-shadow:0 1px 6px rgba(0,0,0,.06)}}
.kpi.q1{{border-color:#00A0DC}}.kpi.q2{{border-color:#E8503A}}.kpi.q3{{border-color:#F5A623}}.kpi.q4{{border-color:#7B7B7B}}
.kpi-label{{font-size:10px;color:#999;margin-bottom:2px}}
.kpi-name{{font-size:13px;font-weight:700;color:#1A1A1A;margin-bottom:6px}}
.kpi-value{{font-size:22px;font-weight:800;color:#1A1A1A;line-height:1}}.kpi-value span{{font-size:11px;font-weight:400;color:#888;margin-left:2px}}
.kpi-sub{{font-size:11px;color:#666;margin-top:5px}}.kpi-sub strong{{color:#1A1A1A}}
.kpi-top{{margin-top:6px;display:flex;flex-wrap:wrap;gap:4px}}
.kpi-tag{{background:#F5F5F5;border-radius:4px;font-size:10px;color:#555;padding:2px 6px}}
.main{{display:flex;gap:14px;align-items:flex-start}}
.chart-wrap{{flex:1;background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.06);padding:16px 12px 8px}}
#chart{{width:100%;height:560px}}
.sidebar{{width:200px;flex-shrink:0;display:flex;flex-direction:column;gap:10px}}
.legend-box{{background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.06);padding:14px}}
.legend-title{{font-size:11px;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}}
.legend-item{{display:flex;align-items:center;gap:7px;margin-bottom:7px}}
.legend-dot{{width:9px;height:9px;border-radius:50%;flex-shrink:0}}
.legend-text{{font-size:11px;color:#444;line-height:1.3}}
.axis-box{{background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.06);padding:14px}}
.axis-title{{font-size:11px;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}}
.axis-item{{margin-bottom:8px}}
.axis-label{{font-size:11px;font-weight:600;color:#444;margin-bottom:2px}}
.axis-desc{{font-size:10px;color:#888;line-height:1.5}}
.filter-row{{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;align-items:center}}
.filter-label{{font-size:11px;color:#888;margin-right:2px}}
.btn{{border:1px solid #E0E0E0;background:#fff;border-radius:6px;padding:4px 10px;font-size:11px;color:#555;cursor:pointer;transition:all .15s}}
.btn:hover{{border-color:#aaa;color:#222}}
.btn.on{{background:#1A1A1A;color:#fff;border-color:#1A1A1A}}
.gtv-btn{{border:1px solid #E0E0E0;background:#fff;border-radius:6px;padding:4px 10px;font-size:11px;color:#555;cursor:pointer;transition:all .15s}}
.gtv-btn:hover{{border-color:#aaa;color:#222}}
.gtv-btn.on{{background:#1A1A1A;color:#fff;border-color:#1A1A1A}}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div>
      <div class="title">520大促 · 三级品类四象限分析</div>
      <div class="subtitle">大促期：5/19–5/20 &nbsp;|&nbsp; 基期：5/12–5/18 &nbsp;|&nbsp; 爆发系数 = 日均大促 / 日均基期 &nbsp;|&nbsp; 阈值：P70</div>
    </div>
    <div class="badge">💕 520大促</div>
  </div>
  <div class="kpi-row" id="kpi-row"></div>
  <div class="filter-row">
    <span class="filter-label">象限筛选：</span>
    <button class="btn on" onclick="fq('all',this)">全部</button>
    <button class="btn" onclick="fq('q1',this)">高GTV高订单</button>
    <button class="btn" onclick="fq('q2',this)">低GTV高订单</button>
    <button class="btn" onclick="fq('q3',this)">高GTV低订单</button>
    <button class="btn" onclick="fq('q4',this)">低GTV低订单</button>
    <span class="filter-label" style="margin-left:8px">GTV规模：</span>
    <button class="gtv-btn on" onclick="fg(0,Infinity,this)">全部</button>
    <button class="gtv-btn" onclick="fg(100,Infinity,this)">&gt;100万</button>
    <button class="gtv-btn" onclick="fg(500,Infinity,this)">&gt;500万</button>
    <button class="gtv-btn" onclick="fg(1000,Infinity,this)">&gt;1000万</button>
  </div>
  <div class="main">
    <div class="chart-wrap">
      <div id="chart"></div>
    </div>
    <div class="sidebar">
      <div class="legend-box">
        <div class="legend-title">品类图例</div>
        <div id="legend-list"></div>
      </div>
      <div class="axis-box">
        <div class="axis-title">指标说明</div>
        <div class="axis-item">
          <div class="axis-label">X轴：GTV爆发系数</div>
          <div class="axis-desc">大促日均闪购GTV ÷ 基期日均闪购GTV，反映消费金额爆发强度</div>
        </div>
        <div class="axis-item">
          <div class="axis-label">Y轴：订单爆发系数</div>
          <div class="axis-desc">大促日均闪购订单量 ÷ 基期日均闪购订单量，反映购买频次爆发强度</div>
        </div>
        <div class="axis-item">
          <div class="axis-label">气泡大小：大促GTV</div>
          <div class="axis-desc">气泡越大代表大促期闪购消费GTV越高</div>
        </div>
        <div class="axis-item" style="margin-top:8px;padding-top:8px;border-top:1px solid #F0F0F0">
          <div class="axis-label" style="color:#888">P70阈值</div>
          <div class="axis-desc">GTV爆发系数 P70 = {XT}<br>订单爆发系数 P70 = {YT}<br>超过P70即为"强爆发"</div>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
const S = {series_json};
const STATS = {stats_json};
const XT={XT}, YT={YT};
const XMIN=0.97, XMAX=8.0, YMIN=0.97, YMAX=8.0;

const legendList = document.getElementById('legend-list');
S.forEach(s => {{
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.innerHTML = `<div class="legend-dot" style="background:${{s.itemStyle.color}}"></div><div class="legend-text">${{s.name}}</div>`;
  legendList.appendChild(item);
}});

const qcfg = [
  {{k:'双强',    cls:'q1', name:'高GTV高订单', desc:'GTV↑↑ 订单↑↑'}},
  {{k:'GTV强',   cls:'q3', name:'高GTV低订单', desc:'GTV↑↑ 订单↑'}},
  {{k:'订单强',  cls:'q2', name:'低GTV高订单', desc:'GTV↑  订单↑↑'}},
  {{k:'稳健增长',cls:'q4', name:'低GTV低订单', desc:'GTV↑  订单↑'}},
];
const kr = document.getElementById('kpi-row');
qcfg.forEach(q => {{
  const d = STATS[q.k];
  kr.innerHTML += `<div class="kpi ${{q.cls}}">
    <div class="kpi-label">${{q.desc}}</div>
    <div class="kpi-name">${{q.name}}</div>
    <div class="kpi-value">${{d.count}}<span>个品类</span></div>
    <div class="kpi-sub">大促GTV：<strong>${{d.gtv.toLocaleString()}} 万</strong></div>
    <div class="kpi-top">${{d.top3.map(t=>`<span class="kpi-tag">${{t}}</span>`).join('')}}</div>
  </div>`;
}});

let chart;

function initChart() {{
  const el = document.getElementById('chart');
  chart = echarts.init(el);
  chart.resize();
  chart.setOption(buildOpt(S));
  setTimeout(() => chart && chart.resize(), 100);
}}

function buildOpt(series) {{
  return {{
    backgroundColor: '#fff',
    grid: {{left:80, right:24, top:44, bottom:80}},
    tooltip: {{
      trigger:'item',
      formatter: p => {{
        const [x,y,gtv]=p.value;
        const gw = gtv>=10000 ? (gtv/10000).toFixed(1)+'万' : gtv.toLocaleString();
        const quad = x>=XT&&y>=YT?'高GTV高订单':x<XT&&y>=YT?'低GTV高订单':x>=XT&&y<YT?'高GTV低订单':'低GTV低订单';
        const qc   = x>=XT&&y>=YT?'#00A0DC':x<XT&&y>=YT?'#E8503A':x>=XT&&y<YT?'#F5A623':'#7B7B7B';
        return `<div style="font-size:13px;font-weight:700;margin-bottom:6px;color:#1A1A1A;border-bottom:1px solid #eee;padding-bottom:6px">${{p.seriesName}} · ${{p.name}}</div>
                <div style="font-size:12px;line-height:2;color:#444">
                  GTV爆发系数：<strong style="color:#1A1A1A">${{x}}</strong><br>
                  订单爆发系数：<strong style="color:#1A1A1A">${{y}}</strong><br>
                  大促消费GTV：<strong style="color:#1A1A1A">${{gw}} 万</strong><br>
                  所属象限：<strong style="color:${{qc}}">${{quad}}</strong>
                </div>`;
      }},
      backgroundColor:'#fff',
      borderColor:'#E0E0E0',borderWidth:1,padding:[10,14],
      extraCssText:'box-shadow:0 4px 20px rgba(0,0,0,.10);border-radius:3px;'
    }},
    legend:{{show:false}},
    xAxis:{{
      type:'value',name:'GTV 爆发系数（闪购）',nameLocation:'middle',nameGap:38,
      nameTextStyle:{{fontSize:11,color:'#888',fontWeight:'500'}},
      min:XMIN,max:XMAX,
      splitLine:{{lineStyle:{{color:'#F0F0F0'}}}},
      axisLine:{{lineStyle:{{color:'#D0D0D0'}}}},axisTick:{{lineStyle:{{color:'#D0D0D0'}}}},axisLabel:{{fontSize:10,color:'#888'}},
    }},
    yAxis:{{
      type:'value',name:'订单量 爆发系数（闪购）',nameLocation:'middle',nameGap:56,
      nameTextStyle:{{fontSize:11,color:'#888',fontWeight:'500'}},
      min:YMIN,max:YMAX,
      splitLine:{{lineStyle:{{color:'#F0F0F0'}}}},
      axisLine:{{lineStyle:{{color:'#D0D0D0'}}}},axisTick:{{lineStyle:{{color:'#D0D0D0'}}}},axisLabel:{{fontSize:10,color:'#888'}},
    }},
    graphic:[
      {{type:'rect',z:-1,left:'8.5%',top:'4%',shape:{{width:'40%',height:'46%'}},style:{{fill:'rgba(123,123,123,0.05)'}}}},
      {{type:'rect',z:-1,left:'48.5%',top:'4%',shape:{{width:'44%',height:'46%'}},style:{{fill:'rgba(245,166,35,0.06)'}}}},
      {{type:'rect',z:-1,left:'8.5%',top:'50%',shape:{{width:'40%',height:'43%'}},style:{{fill:'rgba(232,80,58,0.06)'}}}},
      {{type:'rect',z:-1,left:'48.5%',top:'50%',shape:{{width:'44%',height:'43%'}},style:{{fill:'rgba(0,160,220,0.06)'}}}},
      {{type:'text',z:2,left:'9.5%',top:'5%',style:{{text:'低GTV低订单',fill:'#7B7B7B',fontSize:10,fontWeight:'bold',opacity:.7}}}},
      {{type:'text',z:2,left:'49.5%',top:'5%',style:{{text:'高GTV低订单',fill:'#F5A623',fontSize:10,fontWeight:'bold',opacity:.7}}}},
      {{type:'text',z:2,left:'9.5%',top:'51%',style:{{text:'低GTV高订单',fill:'#E8503A',fontSize:10,fontWeight:'bold',opacity:.7}}}},
      {{type:'text',z:2,left:'49.5%',top:'51%',style:{{text:'高GTV高订单',fill:'#00A0DC',fontSize:10,fontWeight:'bold',opacity:.7}}}},
    ],
    dataZoom:[
      {{type:'inside',xAxisIndex:0,filterMode:'none'}},
      {{type:'inside',yAxisIndex:0,filterMode:'none'}},
    ],
    series: series.map((s,i)=>i===0?{{...s,markLine:{{
      silent:true,symbol:['none','none'],
      lineStyle:{{color:'#BBBBBB',type:'dashed',width:1,opacity:.8}},
      label:{{show:false}},
      data:[{{xAxis:XT}},{{yAxis:YT}}]
    }}}}:s),
  }};
}}

let cq='all', cgMin=0, cgMax=Infinity;

function apply(){{
  const fs=S.map(s=>{{
    const filtered = s.data.filter(d=>{{
      const [x,y,gtv]=d.value;
      const qok=cq==='all'
        ||(cq==='q1'&&x>=XT&&y>=YT)
        ||(cq==='q2'&&x<XT&&y>=YT)
        ||(cq==='q3'&&x>=XT&&y<YT)
        ||(cq==='q4'&&x<XT&&y<YT);
      return qok&&gtv>=cgMin&&gtv<cgMax;
    }});
    return {{...s, data: filtered}};
  }});
  chart.setOption(buildOpt(fs),true);
}}

function fq(q,btn){{
  document.querySelectorAll('.btn').forEach(b=>{{if(b.getAttribute('onclick')?.includes('fq'))b.classList.remove('on');}});
  btn.classList.add('on'); cq=q; apply();
}}

function fg(min,max,btn){{
  document.querySelectorAll('.gtv-btn').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on'); cgMin=min; cgMax=max; apply();
}}

window.addEventListener('resize',()=>chart && chart.resize());

if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', initChart);
}} else {{
  requestAnimationFrame(() => requestAnimationFrame(initChart));
}}
</script>
</body>
</html>'''

output_path = '/Users/lisicong/Desktop/kancong-daily/520大促四象限分析.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML saved: {output_path}")
print(f"Size: {os.path.getsize(output_path)/1024:.1f} KB")
