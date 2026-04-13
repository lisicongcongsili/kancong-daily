-- 520大促爆品分析：2026年5月16日-5月20日，每天TOP商品订单量+品牌新客率
SELECT
    dt,
    product_name,
    brand_name,
    total_orders,
    brand_new_orders,
    brand_new_rate
FROM (
    SELECT
        d.dt,
        d.product_name,
        d.brand_name,
        COUNT(DISTINCT d.order_id) AS total_orders,
        COUNT(DISTINCT CASE WHEN n.is_user_brand_first_order = 1 THEN d.order_id END) AS brand_new_orders,
        ROUND(
            COUNT(DISTINCT CASE WHEN n.is_user_brand_first_order = 1 THEN d.order_id END) * 100.0
            / NULLIF(COUNT(DISTINCT d.order_id), 0),
            2
        ) AS brand_new_rate,
        ROW_NUMBER() OVER (PARTITION BY d.dt ORDER BY COUNT(DISTINCT d.order_id) DESC) AS rn
    FROM mart_lingshou.aggr_ord_order_detail_gtv_dd d
    LEFT JOIN mart_lingshou.aggr_usr_user_poi_gtv_first_order_info_base_dd n
        ON d.order_id = n.order_id
        AND d.dt = n.dt
    WHERE d.dt BETWEEN '20260516' AND '20260520'
      AND d.operate_owner_type_v2_name = '非食专卖业务组'
      AND d.second_owner_name LIKE '%旗舰%'
      AND d.is_arrange = 1
      AND d.product_name IS NOT NULL
      AND d.product_name != ''
    GROUP BY d.dt, d.product_name, d.brand_name
    HAVING COUNT(DISTINCT d.order_id) >= 10
) t
ORDER BY dt ASC, total_orders DESC
