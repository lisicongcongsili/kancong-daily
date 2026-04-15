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

target_brands = list(brand_map.values())
df_target = df[df['brand_name'].isin(target_brands)].copy()
df_target['品牌简称'] = df_target['brand_name'].map({v: k for k, v in brand_map.items()})

# 深度分析：GMV分布 + 店内神券核销情况
for brand_short, brand_full in brand_map.items():
    bdf = df_target[df_target['brand_name'] == brand_full].copy()
    if len(bdf) == 0:
        continue
    
    print(f"{'='*60}")
    print(f"【{brand_short}】")
    
    # GMV分布区间
    bins = [0, 30, 50, 80, 100, 150, 200, 300, 500, 1000, 99999]
    labels = ['0-30', '30-50', '50-80', '80-100', '100-150', '150-200', '200-300', '300-500', '500-1000', '1000+']
    bdf['gmv_range'] = pd.cut(bdf['gmv'], bins=bins, labels=labels)
    gmv_dist = bdf.groupby('gmv_range', observed=True).agg(
        订单数=('order_id', 'count'),
        GMV=('gmv', 'sum')
    )
    gmv_dist['订单占比'] = (gmv_dist['订单数'] / gmv_dist['订单数'].sum() * 100).round(1)
    gmv_dist['GMV占比'] = (gmv_dist['GMV'] / gmv_dist['GMV'].sum() * 100).round(1)
    print(f"\nGMV分布:")
    print(gmv_dist.to_string())
    
    # 店内神券分析（含门槛的券）
    bdf_store = bdf[bdf['coupon_name'].str.contains('店内神券', na=False)].copy()
    if len(bdf_store) > 0:
        print(f"\n店内神券核销 (共{len(bdf_store)}单):")
        store_stats = bdf_store.groupby(['优惠门槛', '优惠面额', 'coupon_name']).agg(
            订单数=('order_id', 'count'),
            GMV均值=('gmv', 'mean'),
            GMV总计=('gmv', 'sum')
        ).reset_index().sort_values('订单数', ascending=False)
        print(store_stats.to_string(index=False))
    
    # 高门槛券（>=99）核销情况
    bdf_high = bdf[bdf['优惠门槛'] >= 99].copy()
    if len(bdf_high) > 0:
        print(f"\n高门槛券(>=99)核销:")
        high_stats = bdf_high.groupby(['优惠门槛', '优惠面额']).agg(
            订单数=('order_id', 'count'),
            GMV均值=('gmv', 'mean'),
        ).reset_index()
        print(high_stats.to_string(index=False))
    
    print()

# 全量数据：店内神券规格汇总
print("\n\n=== 全量旗舰店店内神券规格汇总 ===")
df_store_all = df[df['coupon_name'].str.contains('店内神券', na=False) & df['优惠门槛'].notna()].copy()
store_all_stats = df_store_all.groupby(['优惠门槛', '优惠面额']).agg(
    核销订单数=('order_id', 'count'),
    核销GMV=('gmv', 'sum'),
    均单GMV=('gmv', 'mean'),
    品牌数=('brand_name', 'nunique')
).reset_index()
store_all_stats['折扣率'] = (store_all_stats['优惠面额'] / store_all_stats['优惠门槛'] * 100).round(1)
store_all_stats = store_all_stats.sort_values('核销订单数', ascending=False)
print(store_all_stats.to_string(index=False))
