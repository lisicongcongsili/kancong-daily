WITH qudao AS (
  SELECT DISTINCT qudao, type AS dt_type, user_id, order_id
  FROM upload_table.guanqi_yingxiaoqudao_5
  UNION ALL
  SELECT DISTINCT qudao, type AS dt_type, user_id, order_id
  FROM upload_table.guanqi_yingxiaoqudao_6
),

qudao_ord_list AS (
  SELECT
    CASE 
      WHEN dt BETWEEN 20251027 AND 20251111 THEN '双十一'
      WHEN dt BETWEEN 20251223 AND 20260101 THEN '双旦'
      WHEN dt BETWEEN 20260206 AND 20260214 THEN '年货节'
      WHEN dt BETWEEN 20260305 AND 20260308 THEN '三八'
    END AS dt_type,
    user_id,
    order_id
  FROM mart_lingshou.aggr_ord_order_info_gtv_dd
  WHERE (
    (dt BETWEEN 20251223 AND 20260101) OR
    (dt BETWEEN 20260206 AND 20260214) OR
    (dt BETWEEN 20260305 AND 20260308) OR
    (dt BETWEEN 20251027 AND 20251111)
  )
  AND second_owner_name = '旗舰店业务组'
  AND first_owner_name = '非食专卖业务组'
  GROUP BY
    CASE 
      WHEN dt BETWEEN 20251027 AND 20251111 THEN '双十一'
      WHEN dt BETWEEN 20251223 AND 20260101 THEN '双旦'
      WHEN dt BETWEEN 20260206 AND 20260214 THEN '年货节'
      WHEN dt BETWEEN 20260305 AND 20260308 THEN '三八'
    END,
    user_id,
    order_id
),

target_users AS (
  SELECT DISTINCT
    b.dt_type,
    b.user_id,
    CASE b.dt_type
      WHEN '双十一' THEN '202510'
      WHEN '双旦' THEN '202512'
      WHEN '年货节' THEN '202602'
      WHEN '三八' THEN '202603'
    END AS mo_key,
    CASE b.dt_type
      WHEN '双十一' THEN '2025-10-27'
      WHEN '双旦' THEN '2025-12-23'
      WHEN '年货节' THEN '2026-02-06'
      WHEN '三八' THEN '2026-03-05'
    END AS partition_date_str
  FROM qudao a
  JOIN qudao_ord_list b
    ON a.dt_type = b.dt_type
    AND (
      (a.qudao NOT IN ('外卖柜') AND a.order_id = b.order_id)
      OR
      (a.qudao IN ('外卖柜') AND a.user_id = b.user_id)
    )
  WHERE b.dt_type IS NOT NULL
)

SELECT
  tu.dt_type,
  CASE 
    WHEN yh.age < 18 THEN 'Under 18'
    WHEN yh.age BETWEEN 18 AND 24 THEN '18-24'
    WHEN yh.age BETWEEN 25 AND 34 THEN '25-34'
    WHEN yh.age BETWEEN 35 AND 44 THEN '35-44'
    WHEN yh.age BETWEEN 45 AND 54 THEN '45-54'
    WHEN yh.age BETWEEN 55 AND 64 THEN '55-64'
    ELSE '65+'
  END AS age_group,
  yh.gender,
  yh.city_level,
  yh.is_student,
  yh.is_pregnant,
  shida.score_level,
  shida.crowd_type,
  member.member_name,
  jingzhidu.consume_ability_level_new,
  COUNT(DISTINCT tu.user_id) AS user_cnt
FROM target_users tu
LEFT JOIN mart_lingshou.topic_usr_stp_analyze_user_tag_aggr_d yh
  ON tu.user_id = yh.user_id AND yh.mo = tu.mo_key
LEFT JOIN mart_uzen.ads_user_consume_ability_score_info_df jingzhidu
  ON tu.user_id = jingzhidu.mt_user_id AND jingzhidu.partition_date = tu.partition_date_str
LEFT JOIN mart_lingshou.dwd_member_user_basic_info_df_view member
  ON tu.user_id = member.user_id AND member.partition_date = tu.partition_date_str
LEFT JOIN mart_lingshou.topic_usr_portrait_info_dd shida
  ON tu.user_id = shida.user_id
  AND shida.dt = CASE tu.dt_type
    WHEN '双十一' THEN 20251027
    WHEN '双旦' THEN 20251223
    WHEN '年货节' THEN 20260206
    WHEN '三八' THEN 20260305
  END
GROUP BY
  tu.dt_type,
  CASE 
    WHEN yh.age < 18 THEN 'Under 18'
    WHEN yh.age BETWEEN 18 AND 24 THEN '18-24'
    WHEN yh.age BETWEEN 25 AND 34 THEN '25-34'
    WHEN yh.age BETWEEN 35 AND 44 THEN '35-44'
    WHEN yh.age BETWEEN 45 AND 54 THEN '45-54'
    WHEN yh.age BETWEEN 55 AND 64 THEN '55-64'
    ELSE '65+'
  END,
  yh.gender,
  yh.city_level,
  yh.is_student,
  yh.is_pregnant,
  shida.score_level,
  shida.crowd_type,
  member.member_name,
  jingzhidu.consume_ability_level_new
ORDER BY tu.dt_type, user_cnt DESC
