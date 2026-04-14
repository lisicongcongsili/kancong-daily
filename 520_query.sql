with gmv as (
  SELECT gmv.dt,
         prod_first_category_name,
         prod_second_category_name,
         prod_third_category_name,
         SUM(actual_price) AS actual_total_price,
         COUNT(DISTINCT order_id) AS order_cnt,
         SUM(nmd_no_areabrand_charge_amt) as meibu_gmv,
         SUM(if(first_owner_name_dbr_pvt = '非食专卖',actual_price,0)) AS feishi_actual_total_price,
         COUNT(DISTINCT if(first_owner_name_dbr_pvt = '非食专卖',order_id,null)) AS feishi_order_cnt,
         SUM(if(first_owner_name_dbr_pvt = '非食专卖',nmd_no_areabrand_charge_amt,0)) as feishi_meibu_gmv
    FROM mart_lingshou.dws_ord_order_gmv_detail_private_category_res_di gmv
   WHERE gmv.dt BETWEEN '20250512' AND '20250520'
     AND gmv.prod_first_category_name IN ('手机通讯','电脑数码','母婴用品','美容护肤','宠物生活','彩妆香水','个人洗护','服饰鞋包','家用电器','家居日用','运动户外','学习/办公用品','家装建材','玩具乐器','厨具餐具','家庭清洁','节庆礼品','家纺布艺','成人用品','珠宝首饰')
   GROUP BY 1,2,3,4
),
shangpin_baoguang as (
  select dt,
         product_first_category_name as prod_first_category_name,
         product_second_category_name as prod_second_category_name,
         product_third_category_name as prod_third_category_name,
         sum(if_view_cnt_m) as if_view_cnt_m_uv,
         sum(if_click_cnt_m) as if_click_cnt_m_uv,
         sum(if_ord_cnt_gmv) as if_ord_cnt_gmv_uv,
         sum(feishi_if_view_cnt_m) as feishi_if_view_cnt_m,
         sum(feishi_if_click_cnt_m) as feishi_if_click_cnt_m,
         sum(feishi_if_ord_cnt_gmv) as feishi_if_ord_cnt_gmv
    from (
          SELECT union_id,
                 dt,
                 product_first_category_name,
                 product_second_category_name,
                 product_third_category_name,
                 max(if(view_cnt_m>0,1,0)) as if_view_cnt_m,
                 max(if(click_cnt_m>0,1,0)) as if_click_cnt_m,
                 max(if(ord_cnt_gmv>0,1,0)) as if_ord_cnt_gmv,
                 max(if(first_owner_name = '非食专卖业务组' and view_cnt_m>0,1,0)) as feishi_if_view_cnt_m,
                 max(if(first_owner_name = '非食专卖业务组' and click_cnt_m>0,1,0)) as feishi_if_click_cnt_m,
                 max(if(first_owner_name = '非食专卖业务组' and ord_cnt_gmv>0,1,0)) as feishi_if_ord_cnt_gmv
            FROM mart_lingshou.topic_flow_prod_mvmc_and_transform_info_sd
           WHERE dt BETWEEN '20250512' AND '20250520'
             AND product_first_category_name IN ('手机通讯','电脑数码','母婴用品','美容护肤','宠物生活','彩妆香水','个人洗护','服饰鞋包','家用电器','家居日用','运动户外','学习/办公用品','家装建材','玩具乐器','厨具餐具','家庭清洁','节庆礼品','家纺布艺','成人用品','珠宝首饰')
             AND entry_name LIKE '%搜索%'
           GROUP BY 1,2,3,4,5
         )a
   group by 1,2,3,4
),
sousuo_qv as (
  SELECT dt,
         query_max_spu_first_classify AS prod_first_category_name,
         query_max_spu_second_classify AS prod_second_category_name,
         query_max_spu_third_classify AS prod_third_category_name,
         COUNT(DISTINCT view_sg_m_uid) AS ss_view_uv,
         COUNT(DISTINCT ord_gmv_uid) AS ss_ord_uv
    FROM mart_lingshou.topic_flow_search_word_mvmc_and_transfrom_sd
   WHERE dt BETWEEN '20250512' AND '20250520'
     AND is_query_sg_strong_intent = 1
     AND query_intent_result = '商品意图'
     AND source_channel_id IN (1,2,4)
     AND query_max_spu_first_classify IN ('手机通讯','电脑数码','母婴用品','美容护肤','宠物生活','彩妆香水','个人洗护','服饰鞋包','家用电器','家居日用','运动户外','学习/办公用品','家装建材','玩具乐器','厨具餐具','家庭清洁','节庆礼品','家纺布艺','成人用品','珠宝首饰')
   GROUP BY 1,2,3,4
)
select dt,
       prod_first_category_name,
       prod_second_category_name,
       prod_third_category_name,
       sum(order_cnt) as order_cnt,
       sum(actual_total_price) as actual_total_price,
       sum(if_view_cnt_m_uv) as if_view_cnt_m_uv,
       sum(if_ord_cnt_gmv_uv) as if_ord_cnt_gmv_uv,
       sum(feishi_order_cnt) as feishi_order_cnt,
       sum(feishi_actual_total_price) as feishi_actual_total_price,
       sum(feishi_if_view_cnt_m) as feishi_if_view_cnt_m,
       sum(feishi_if_ord_cnt_gmv) as feishi_if_ord_cnt_gmv,
       sum(ss_view_uv) as ss_view_uv,
       sum(ss_ord_uv) as ss_ord_uv
  from (
        select dt, prod_first_category_name, prod_second_category_name, prod_third_category_name,
               actual_total_price, order_cnt, meibu_gmv, feishi_actual_total_price, feishi_order_cnt, feishi_meibu_gmv,
               0 as if_view_cnt_m_uv, 0 as if_click_cnt_m_uv, 0 as if_ord_cnt_gmv_uv,
               0 as feishi_if_view_cnt_m, 0 as feishi_if_click_cnt_m, 0 as feishi_if_ord_cnt_gmv,
               0 as ss_view_uv, 0 as ss_ord_uv
          from gmv
     union all
        select dt, prod_first_category_name, prod_second_category_name, prod_third_category_name,
               0,0,0,0,0,0,
               if_view_cnt_m_uv, if_click_cnt_m_uv, if_ord_cnt_gmv_uv,
               feishi_if_view_cnt_m, feishi_if_click_cnt_m, feishi_if_ord_cnt_gmv,
               0,0
          from shangpin_baoguang
     union all
        select dt, prod_first_category_name, prod_second_category_name, prod_third_category_name,
               0,0,0,0,0,0,0,0,0,0,0,0,
               ss_view_uv, ss_ord_uv
          from sousuo_qv
       )a
 group by 1,2,3,4
