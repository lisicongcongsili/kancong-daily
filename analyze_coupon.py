import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

file = '/Users/lisicong/Desktop/旗舰店神券核销（2月13日-4月13日）.xlsx'
df = pd.read_excel(file, sheet_name='Sheet1')

# 只看付款成功的订单 (pay_status=3)
df = df[df['pay_status'] == 3].copy()

# 目标品牌映射
brand_map = {
    '全棉时代': '全棉时代(官方旗舰店)',
    '闪迪': '闪迪官方旗舰店',
    '薇诺娜': 'WINONA官方旗舰店',
    '小野和子': '小野和子官方旗舰店',
    'babycare': 'Babycare官方旗舰店',
}

# 筛选目标品牌
target_brands = list(brand_map.values())
df_target = df[df['brand_name'].isin(target_brands)].copy()
df_target['品牌简称'] = df_target['brand_name'].map({v: k for k, v in brand_map.items()})

print(f"目标品牌总订单数: {len(df_target)}")
print()

# 按品牌分析
for brand_short, brand_full in brand_map.items():
    bdf = df_target[df_target['brand_name'] == brand_full].copy()
    if len(bdf) == 0:
        print(f"【{brand_short}】无数据")
        continue
    
    # 只看有门槛的券（排除神会员等无门槛券）
    bdf_coupon = bdf[bdf['优惠门槛'].notna() & bdf['优惠面额'].notna()].copy()
    
    print(f"{'='*60}")
    print(f"【{brand_short}】 总订单: {len(bdf)}, 有门槛券订单: {len(bdf_coupon)}")
    print(f"  GMV: 总={bdf['gmv'].sum():.0f}, 均值={bdf['gmv'].mean():.1f}, 中位数={bdf['gmv'].median():.1f}")
    print(f"  GMV分布: p25={bdf['gmv'].quantile(0.25):.1f}, p75={bdf['gmv'].quantile(0.75):.1f}, p90={bdf['gmv'].quantile(0.90):.1f}")
    
    if len(bdf_coupon) > 0:
        print(f"\n  有门槛券分析:")
        print(f"  门槛分布: {sorted(bdf_coupon['优惠门槛'].unique().tolist())}")
        print(f"  面额分布: {sorted(bdf_coupon['优惠面额'].unique().tolist())}")
        
        # 按门槛+面额分组统计
        coupon_stats = bdf_coupon.groupby(['优惠门槛', '优惠面额']).agg(
            核销订单数=('order_id', 'count'),
            核销GMV=('gmv', 'sum'),
            均单GMV=('gmv', 'mean'),
        ).reset_index()
        coupon_stats['折扣率'] = (coupon_stats['优惠面额'] / coupon_stats['优惠门槛'] * 100).round(1)
        coupon_stats = coupon_stats.sort_values('核销订单数', ascending=False)
        print(f"\n  券规格核销明细:")
        print(coupon_stats.to_string(index=False))
    
    # 券名分析
    print(f"\n  券名TOP10:")
    coupon_name_stats = bdf.groupby('coupon_name').agg(
        订单数=('order_id', 'count'),
        GMV=('gmv', 'sum')
    ).sort_values('订单数', ascending=False).head(10)
    print(coupon_name_stats.to_string())
    print()
