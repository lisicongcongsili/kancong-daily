SELECT
    query_max_spu_first_classify  AS prod_first_category_name,
    query_max_spu_second_classify AS prod_second_category_name,
    query_max_spu_third_classify  AS prod_third_category_name,
    COUNT(DISTINCT view_sg_m_uid) AS base_ss_view_uv_total,
    COUNT(DISTINCT view_sg_m_uid) / 7.0 AS base_ss_view_uv_avg
FROM mart_lingshou.topic_flow_search_word_mvmc_and_transfrom_sd
WHERE dt BETWEEN '20250512' AND '20250518'
  AND is_query_sg_strong_intent = 1
  AND query_intent_result = '商品意图'
  AND source_channel_id IN (1, 2, 4)
  AND query_max_spu_first_classify IN (
    '手机通讯','电脑数码','母婴用品','美容护肤','宠物生活','彩妆香水',
    '个人洗护','服饰鞋包','家用电器','家居日用','运动户外','学习/办公用品',
    '家装建材','玩具乐器','厨具餐具','家庭清洁','节庆礼品','家纺布艺',
    '成人用品','珠宝首饰'
  )
GROUP BY 1, 2, 3
