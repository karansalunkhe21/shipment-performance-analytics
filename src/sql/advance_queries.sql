-- =============================================================================
-- Shipment Performance Analytics — Advanced SQL Queries
-- Techniques: CTEs, Window Functions, RANK(), LAG(), PARTITION BY
-- =============================================================================


-- -----------------------------------------------------------------------------
-- QUERY 1: Running Total of Revenue by Month
-- Technique: CTE + Window Function (SUM OVER)
-- -----------------------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT
        strftime('%Y', order_date_dateorders)  AS year,
        strftime('%m', order_date_dateorders)  AS month,
        ROUND(SUM(sales), 2)                   AS total_revenue
    FROM shipments
    GROUP BY year, month
)
SELECT
    year,
    month,
    total_revenue,
    ROUND(SUM(total_revenue) OVER (
        ORDER BY year, month
    ), 2)                                      AS running_total
FROM monthly_revenue
ORDER BY year, month;


-- -----------------------------------------------------------------------------
-- QUERY 2: Rank Shipping Modes by Revenue
-- Technique: CTE + RANK() Window Function
-- -----------------------------------------------------------------------------
WITH shipping_revenue AS (
    SELECT
        shipping_mode,
        ROUND(SUM(sales), 2)                  AS total_revenue,
        ROUND(SUM(order_profit_per_order), 2) AS total_profit,
        COUNT(*)                              AS total_orders
    FROM shipments
    GROUP BY shipping_mode
)
SELECT
    shipping_mode,
    total_revenue,
    total_profit,
    total_orders,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM shipping_revenue;


-- -----------------------------------------------------------------------------
-- QUERY 3: Month over Month Revenue Growth
-- Technique: CTE + LAG() Window Function
-- -----------------------------------------------------------------------------
WITH monthly AS (
    SELECT
        strftime('%Y', order_date_dateorders) AS year,
        strftime('%m', order_date_dateorders) AS month,
        ROUND(SUM(sales), 2)                  AS revenue
    FROM shipments
    GROUP BY year, month
)
SELECT
    year,
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY year, month)  AS prev_month_revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year, month))
          / LAG(revenue) OVER (ORDER BY year, month), 2) AS mom_growth_pct
FROM monthly
ORDER BY year, month;


-- -----------------------------------------------------------------------------
-- QUERY 4: Top 3 Products per Category by Revenue
-- Technique: CTE + RANK() with PARTITION BY
-- -----------------------------------------------------------------------------
WITH product_revenue AS (
    SELECT
        category_name,
        product_name,
        ROUND(SUM(sales), 2) AS total_revenue,
        COUNT(*)             AS total_orders
    FROM shipments
    GROUP BY category_name, product_name
),
ranked AS (
    SELECT
        category_name,
        product_name,
        total_revenue,
        total_orders,
        RANK() OVER (
            PARTITION BY category_name
            ORDER BY total_revenue DESC
        ) AS rank_in_category
    FROM product_revenue
)
SELECT *
FROM ranked
WHERE rank_in_category <= 3
ORDER BY category_name, rank_in_category;


-- -----------------------------------------------------------------------------
-- QUERY 5: Customers who Experienced Delivery Deterioration
-- Technique: Multiple CTEs + Self JOIN
-- -----------------------------------------------------------------------------
WITH customer_yearly AS (
    SELECT
        order_customer_id,
        strftime('%Y', order_date_dateorders)       AS year,
        ROUND(100.0 * SUM(is_late) / COUNT(*), 2)  AS late_rate
    FROM shipments
    GROUP BY order_customer_id, year
),
comparison AS (
    SELECT
        a.order_customer_id,
        a.late_rate AS late_rate_2015,
        b.late_rate AS late_rate_2017,
        ROUND(b.late_rate - a.late_rate, 2) AS deterioration
    FROM customer_yearly a
    JOIN customer_yearly b
        ON a.order_customer_id = b.order_customer_id
        AND a.year = '2015'
        AND b.year = '2017'
)
SELECT *
FROM comparison
WHERE deterioration > 20
ORDER BY deterioration DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 6: Revenue Contribution % per Category
-- Technique: CTE + SUM OVER (no partition) for grand total
-- -----------------------------------------------------------------------------
WITH category_revenue AS (
    SELECT
        category_name,
        ROUND(SUM(sales), 2) AS total_revenue
    FROM shipments
    GROUP BY category_name
)
SELECT
    category_name,
    total_revenue,
    ROUND(100.0 * total_revenue / SUM(total_revenue) OVER (), 2) AS revenue_contribution_pct
FROM category_revenue
ORDER BY revenue_contribution_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 7: Late Delivery Rate Moving Average (3 Month)
-- Technique: CTE + AVG OVER with ROWS BETWEEN
-- -----------------------------------------------------------------------------
WITH monthly_late AS (
    SELECT
        strftime('%Y', order_date_dateorders)        AS year,
        strftime('%m', order_date_dateorders)        AS month,
        ROUND(100.0 * SUM(is_late) / COUNT(*), 2)   AS late_rate_pct
    FROM shipments
    GROUP BY year, month
)
SELECT
    year,
    month,
    late_rate_pct,
    ROUND(AVG(late_rate_pct) OVER (
        ORDER BY year, month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                                            AS moving_avg_3month
FROM monthly_late
ORDER BY year, month;


-- -----------------------------------------------------------------------------
-- QUERY 8: Customer Lifetime Value (CLV) Ranking
-- Technique: CTE + RANK() + NTILE()
-- -----------------------------------------------------------------------------
WITH customer_value AS (
    SELECT
        order_customer_id,
        COUNT(*)                                AS total_orders,
        ROUND(SUM(sales), 2)                   AS total_revenue,
        ROUND(SUM(order_profit_per_order), 2)  AS total_profit,
        ROUND(AVG(sales), 2)                   AS avg_order_value
    FROM shipments
    GROUP BY order_customer_id
)
SELECT
    order_customer_id,
    total_orders,
    total_revenue,
    total_profit,
    avg_order_value,
    RANK() OVER (ORDER BY total_revenue DESC)     AS revenue_rank,
    NTILE(4) OVER (ORDER BY total_revenue DESC)   AS customer_tier
FROM customer_value
ORDER BY revenue_rank
LIMIT 20;


---  Product Performance with Revenue Rank and Cumulative Revenue
WITH product_stats AS (
    SELECT
        product_name,
        COUNT(*)                                        AS total_orders,
        ROUND(SUM(sales), 2)                           AS total_revenue,
        ROUND(SUM(order_profit_per_order), 2)          AS total_profit,
        ROUND(100.0 * SUM(is_late) / COUNT(*), 2)      AS late_rate_pct
    FROM shipments
    GROUP BY product_name
)
SELECT
    product_name,
    total_orders,
    total_revenue,
    total_profit,
    late_rate_pct,
    RANK() OVER (ORDER BY total_revenue DESC)          AS revenue_rank,
    ROUND(SUM(total_revenue) OVER (
        ORDER BY total_revenue DESC
    ), 2)                                              AS cumulative_revenue
FROM product_stats
LIMIT 15;


--- Top 3 Markets per Year by Revenue using PARTITION BY

WITH yearly_market AS (
    SELECT
        strftime('%Y', order_date_dateorders)   AS year,
        market,
        ROUND(SUM(sales), 2)                   AS total_revenue
    FROM shipments
    GROUP BY year, market
),
ranked AS (
    SELECT
        year,
        market,
        total_revenue,
        RANK() OVER (
            PARTITION BY year
            ORDER BY total_revenue DESC
        )                                       AS market_rank
    FROM yearly_market
)
SELECT *
FROM ranked
WHERE market_rank <= 3
ORDER BY year, market_rank;