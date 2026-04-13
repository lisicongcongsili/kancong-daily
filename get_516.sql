SELECT * FROM (
    SELECT
        t.prod_third_category_name,
        t.product_name,
        t.brand_name,
        SUM(CASE WHEN t.dt BETWEEN '20250516' AND '20250520' THEN t.product_actual_price ELSE 0 END) AS promo_gtv,
        SUM(CASE WHEN t.dt BETWEEN '20250516' AND '20250520' THEN 1 ELSE 0 END) AS promo_order_cnt,
        SUM(CASE WHEN t.dt BETWEEN '20250509' AND '20250515' THEN t.product_actual_price ELSE 0 END) AS base_gtv,
        SUM(CASE WHEN t.dt BETWEEN '20250509' AND '20250515' THEN 1 ELSE 0 END) AS base_order_cnt,
        SUM(CASE WHEN t.dt BETWEEN '20250516' AND '20250520' THEN t.product_actual_price ELSE 0 END) / 5.0 AS promo_daily_gtv,
        SUM(CASE WHEN t.dt BETWEEN '20250509' AND '20250515' THEN t.product_actual_price ELSE 0 END) / 7.0 AS base_daily_gtv,
        SUM(CASE WHEN t.dt BETWEEN '20250516' AND '20250520' THEN t.product_actual_price ELSE 0 END) / NULLIF(SUM(CASE WHEN t.dt BETWEEN '20250516' AND '20250520' THEN 1 ELSE 0 END), 0) AS promo_avg_price,
        SUM(CASE WHEN t.dt BETWEEN '20250509' AND '20250515' THEN t.product_actual_price ELSE 0 END) / NULLIF(SUM(CASE WHEN t.dt BETWEEN '20250509' AND '20250515' THEN 1 ELSE 0 END), 0) AS base_avg_price
    FROM mart_lingshou.aggr_ord_order_detail_gtv_dd t
    WHERE t.dt BETWEEN '20250509' AND '20250520'
      AND t.operate_owner_type_v2_name = '非食专卖业务组'
      AND t.prod_third_category_name IN ('卸妆','洁面','防晒霜/乳/喷雾','女士内裤','其他户外装备','移动电源','一次性内衣/内裤','一次性毛巾浴巾','女士拖鞋','烧烤用品','一次性床品套件','面部护理套装','女士泳衣','帐篷','乳贴','洗漱旅行便携装','牙刷','男士拖鞋','座椅板凳','假睫毛及工具','粉底液/膏','浴室用品','男士泳衣','帽子','面部喷雾','其他玩具','儿童驱蚊用品','桌类','烧烤用具','野餐垫/防潮垫','储存卡','钓箱钓椅','美发工具','女士凉鞋','脱毛膏/脱毛蜡纸','蜜粉/散粉','卷发/直发器','扑克','皮肤衣/防晒衣','美妆蛋/粉扑','单肩包/斜挎包','照明设备','气垫BB/BB霜','双眼皮贴/双眼皮胶','眼线笔/眼线液','泳镜','卫生棉条','文胸','隔离/妆前','冲锋衣裤','高光/修容','手机拍照配件','抹胸','桌游','其他钓鱼配件','钓竿','麻将','电动/遥控玩具','睫毛膏/睫毛增长液','婴儿推车','化妆刷','儿童口腔护理','其他游泳用品','化妆镜','手持风扇','儿童雨衣/雨靴','穿戴甲','鱼饵','读卡器','宝宝防晒霜','防晒帽/面罩/口罩','儿童拖鞋','儿童内衣裤','金条/金豆/金砖类','戏水玩具','游泳圈','定妆喷雾','泳帽','保暖内衣套装','一次性袜子','眼镜盒/眼镜框架','服饰配件','儿童套装','男士凉鞋','腮红/胭脂','睫毛夹','筹码','宝宝洗发沐浴二合一','游戏手柄/方向盘','儿童裤装','拍立得','儿童T恤','玩具枪','沙滩鞋','儿童帽子','指甲油','睡袋','儿童外套','儿童裙子','儿童凉鞋','女士雨鞋','吊床','一次性拖鞋','宝宝浴盆','其他棋牌麻将/工具','男士素颜霜','鱼线','其他喂养用品','游戏机','女士靴子','对讲机','钓鱼服饰','腰凳/背带','奶瓶果蔬清洗液','游戏软件','挂脖风扇','肩带','婴童口水巾/围嘴/围兜','睡袍/浴袍','其他出行装备','攀岩装备','手机防水袋','溯溪鞋','儿童坐便器','应急灯','锅具套装')
    GROUP BY t.prod_third_category_name, t.product_name, t.brand_name
) sub
WHERE sub.promo_gtv >= 5000
ORDER BY sub.promo_gtv DESC
LIMIT 500
