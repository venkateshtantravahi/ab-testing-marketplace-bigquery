--  Compute group-level KPIs segmented by product category and customer state
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.segment_kpis` AS
WITH base AS (
    SELECT
        og.ab_group,
        c.customer_state,
        p.product_category_name,
        o.order_id,
        o.order_status,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        pay.payment_value,
        r.review_score,
        r.review_id
    FROM `ab-testing-analytics.marketplace_ab_test.orders_with_groups` og
    JOIN `ab-testing-analytics.marketplace_ab_test.orders` o on og.order_id = o.order_id
    JOIN `ab-testing-analytics.marketplace_ab_test.customers` c on o.customer_id = c.customer_id
    JOIN `ab-testing-analytics.marketplace_ab_test.order_items` oi on o.order_id = oi.order_id
    JOIN `ab-testing-analytics.marketplace_ab_test.products` p on oi.product_id = p.product_id
    LEFT JOIN `ab-testing-analytics.marketplace_ab_test.payments` pay on o.order_id = pay.order_id
    LEFT JOIN `ab-testing-analytics.marketplace_ab_test.reviews` r on o.order_id = r.order_id
)

SELECT
    ab_group,
    customer_state,
    product_category_name,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNTIF(order_status = 'Delivered') AS delivered_orders,
    ROUND((COUNTIF(order_status = 'delivered') * 1.0 / COUNT(DISTINCT order_id)), 3) AS conversion_rate,
    ROUND(AVG(payment_value), 2) AS avg_order_value,
    ROUND(AVG(TIMESTAMP_DIFF(order_purchase_timestamp, order_delivered_customer_date, DAY)), 2) AS avg_delivery_days,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(COUNT(DISTINCT review_id) * 1.0 / COUNT(DISTINCT order_id), 3) AS review_rate
FROM base
GROUP BY ab_group, customer_state, product_category_name
ORDER BY ab_group, customer_state, product_category_name;

