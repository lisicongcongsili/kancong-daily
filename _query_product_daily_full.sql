-- by天商品数据，2025-10-01至今，每天TOP商品订单量+品牌新客率
SELECT
    dt,
    product_name,
    brand_name,
    SUM(total_orders) AS total_orders,
    SUM(brand_new_orders) AS brand_new_orders,
    ROUND(SUM(brand_new_orders) * 100.0 / NULLIF(SUM(total_orders), 0), 2) AS brand_new_rate
FROM (
    SELECT
        o.dt,
        g.spu_name AS product_name,
        g.brand_name,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT CASE WHEN n.is_user_brand_first_order = 1 THEN o.order_id END) AS brand_new_orders
    FROM mart_lingshou.aggr_ord_order_detail_gtv_dd o
    JOIN mart_lingshou.aggr_ord_order_info_gtv_dd oi
        ON o.order_id = oi.order_id AND o.dt = oi.dt
    LEFT JOIN mart_lingshou.aggr_usr_user_poi_gtv_first_order_info_base_dd n
        ON o.order_id = n.order_id AND o.dt = n.dt
    LEFT JOIN mart_lingshou.dim_lingshou_goods_info g
        ON o.goods_id = g.goods_id
    WHERE o.dt >= '20251001'
      AND o.dt <= '20260401'
      AND oi.first_owner_name = '非食专卖业务组'
      AND oi.second_owner_name LIKE '%旗舰%'
      AND oi.is_arrange = 1
    GROUP BY o.dt, g.spu_name, g.brand_name
) t
GROUP BY dt, product_name, brand_name
ORDER BY dt, total_orders DESC
