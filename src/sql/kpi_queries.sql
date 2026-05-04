-- =====================================================
-- Shipment Performance Analytics — KPI Queries
-- =====================================================

-- KPI 1: Overall On-Time Delivery Rate
SELECT
    COUNT(*)                                                         AS total_orders,
    SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END)                   AS on_time_orders,
    SUM(is_late)                                                     AS late_orders,
    ROUND(100.0 * SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
                                                                     AS otd_pct
FROM shipments;


-- KPI 2: OTD% by Shipping Mode
SELECT
    shipping_mode,
    COUNT(*)                                                         AS total_orders,
    SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END)                   AS on_time_orders,
    ROUND(100.0 * SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
                                                                     AS otd_pct
FROM shipments
GROUP BY shipping_mode
ORDER BY otd_pct DESC;


-- KPI 3: OTD% by Region
SELECT
    order_region,
    COUNT(*)                                                         AS total_orders,
    SUM(is_late)                                                     AS late_orders,
    ROUND(100.0 * SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
                                                                     AS otd_pct
FROM shipments
GROUP BY order_region
ORDER BY otd_pct ASC;


-- KPI 4: Revenue and Profit by Category
SELECT
    category_name,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(sales), 2)                   AS total_revenue,
    ROUND(SUM(order_profit_per_order), 2)  AS total_profit,
    ROUND(100.0 * SUM(order_profit_per_order) / SUM(sales), 2) AS profit_margin_pct
FROM shipments
GROUP BY category_name
ORDER BY total_revenue DESC;

-- KPI 5: Impact of Discount on Profit Margin
SELECT
    CASE
        WHEN order_item_discount_rate = 0        THEN 'No Discount'
        WHEN order_item_discount_rate <= 0.05    THEN '0-5%'
        WHEN order_item_discount_rate <= 0.10    THEN '5-10%'
        WHEN order_item_discount_rate <= 0.20    THEN '10-20%'
        ELSE 'Above 20%'
    END                                            AS discount_band,
    COUNT(*)                                       AS total_orders,
    ROUND(AVG(order_profit_per_order), 2)          AS avg_profit,
    ROUND(AVG(sales), 2)                           AS avg_sales
FROM shipments
GROUP BY discount_band
ORDER BY avg_profit DESC;