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

# 查看店内神券的coupon_name样本
print("=== 含'神券'的coupon_name样本 ===")
coupon_samples = df[df['coupon_name'].str.contains('神券', na=False)]['coupon_name'].value_counts().head(30)
print(coupon_samples.to_string())

print("\n=== 含门槛的券名样本 ===")
df_with_threshold = df[df['优惠门槛'].notna() & df['优惠面额'].notna()]
print(f"有门槛券总订单数: {len(df_with_threshold)}")
coupon_threshold_samples = df_with_threshold['coupon_name'].value_counts().head(30)
print(coupon_threshold_samples.to_string())

print("\n=== 有门槛券的门槛+面额分布（全量）===")
all_coupon_stats = df_with_threshold.groupby(['优惠门槛', '优惠面额']).agg(
    核销订单数=('order_id', 'count'),
    核销GMV=('gmv', 'sum'),
    均单GMV=('gmv', 'mean'),
    品牌数=('brand_name', 'nunique')
).reset_index()
all_coupon_stats['折扣率'] = (all_coupon_stats['优惠面额'] / all_coupon_stats['优惠门槛'] * 100).round(1)
all_coupon_stats = all_coupon_stats.sort_values('核销订单数', ascending=False)
print(all_coupon_stats.head(30).to_string(index=False))
