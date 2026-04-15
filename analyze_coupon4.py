import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

file = '/Users/lisicong/Desktop/旗舰店神券核销（2月13日-4月13日）.xlsx'
df = pd.read_excel(file, sheet_name='Sheet1')
df = df[df['pay_status'] == 3].copy()

brand_map = {
    '全棉时代': '全棉时代(官方旗舰店)',
    '闪迪': '闪迪官方旗舰店',
    '薇诺娜': 'WINONA官方旗舰店',
    '小野和子': '小野和子官方旗舰店',
    'babycare': 'Babycare官方旗舰店',
}

# 核心分析：各品牌的店内神券（coupon_name含"神券"且有门槛）核销情况
# 以及各品牌的GMV分布，用于推算合理门槛

print("=== 各品牌店内神券核销详情 ===")
for brand_short, brand_full in brand_map.items():
    bdf = df[df['brand_name'] == brand_full].copy()
    
    # 店内神券（含门槛）
    bdf_store = bdf[bdf['coupon_name'].str.contains('店内神券', na=False)].copy()
    
    print(f"\n【{brand_short}】 总订单={len(bdf)}, 店内神券订单={len(bdf_store)}")
    
    if len(bdf_store) > 0:
        coupon_detail = bdf_store.groupby('coupon_name').agg(
            订单数=('order_id', 'count'),
            GMV均值=('gmv', 'mean'),
            GMV中位数=('gmv', 'median'),
            GMV总计=('gmv', 'sum'),
        ).sort_values('订单数', ascending=False)
        print(coupon_detail.to_string())
    
    # 各GMV区间的订单占比（用于判断门槛设置）
    print(f"\n  GMV分位数: p50={bdf['gmv'].quantile(0.5):.1f}, p60={bdf['gmv'].quantile(0.6):.1f}, p70={bdf['gmv'].quantile(0.7):.1f}, p80={bdf['gmv'].quantile(0.8):.1f}, p90={bdf['gmv'].quantile(0.9):.1f}")
    
    # 各门槛覆盖率
    for threshold in [49, 59, 69, 79, 99, 139, 199, 299]:
        coverage = (bdf['gmv'] >= threshold).sum() / len(bdf) * 100
        print(f"  GMV>={threshold}的订单占比: {coverage:.1f}%")

print("\n\n=== 全量旗舰店各神券规格核销量（含名称中有门槛数字的）===")
# 从coupon_name中提取门槛信息
df_store_named = df[df['coupon_name'].str.contains('店内神券', na=False)].copy()
print(f"店内神券总订单: {len(df_store_named)}")
coupon_name_stats = df_store_named.groupby('coupon_name').agg(
    订单数=('order_id', 'count'),
    GMV均值=('gmv', 'mean'),
    GMV总计=('gmv', 'sum'),
    品牌数=('brand_name', 'nunique')
).sort_values('订单数', ascending=False)
print(coupon_name_stats.to_string())
