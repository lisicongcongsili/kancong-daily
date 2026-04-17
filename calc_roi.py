import pandas as pd

df = pd.read_excel('/Users/lisicong/Desktop/渠道营销大表.xlsx', header=None)
cols = df.iloc[0].tolist()
df.columns = cols
df = df.iloc[1:].reset_index(drop=True)

综合 = df[df['节促'] == '综合'].copy()

for _, r in 综合.iterrows():
    name = r['渠道']
    budget = r['预算消耗（万）']
    guanqi_gtv = r['官旗消费GTV']
    feishi_gtv = r['非食消费GTV']
    guanqi_orders = r['官旗订单量']
    brand_new = r['官旗品牌新用户数量']
    brand_new_pct = r['官旗品牌新用户占比']
    r7 = r['下单用户7日内官旗复购率🌟']
    r60 = r['下单用户60日内官旗复购率🌟']
    gtv_g60 = r['下单用户60日内官旗人均消费GTV']
    gtv_f60 = r['60日内非食人均消费GTV']
    gtv_s60 = r['下单用户60日内闪购人均消费GTV']

    def safe_float(v):
        try:
            return float(v)
        except:
            return None

    b = safe_float(budget)
    g = safe_float(guanqi_gtv)
    f = safe_float(feishi_gtv)

    guanqi_roi = round(g / 10000 / b, 2) if b and g and b > 0 else '-'
    feishi_roi = round(f / 10000 / b, 2) if b and f and b > 0 else '-'

    def fmt_pct(v):
        v2 = safe_float(v)
        return f"{round(v2*100,1)}%" if v2 is not None else '-'

    def fmt_val(v, div=1):
        v2 = safe_float(v)
        return round(v2/div, 1) if v2 is not None else '-'

    print(f"【{name}】预算:{budget}万 | 官旗订单:{guanqi_orders} | 官旗GTV:{fmt_val(g,10000)}万 | 官旗ROI:{guanqi_roi} | 非食GTV:{fmt_val(f,10000)}万 | 非食ROI:{feishi_roi} | 品牌新客:{brand_new}({fmt_pct(brand_new_pct)}) | 7日官旗复购:{fmt_pct(r7)} | 60日官旗复购:{fmt_pct(r60)} | 官旗60日人均:{fmt_val(gtv_g60)}元 | 非食60日人均:{fmt_val(gtv_f60)}元 | 闪购60日人均:{fmt_val(gtv_s60)}元")
