-- Compute A/B group-level KPIs for conversion, value, delivery, satisfaction
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.ab_group_metrics` AS
SELECT
  og.ab_group,
  COUNT(DISTINCT o.order_id) AS total_orders,
  COUNTIF(o.order_status = 'delivered') AS delivered_orders,
  ROUND(COUNTIF(o.order_status = 'delivered') * 1.0 / COUNT(DISTINCT o.order_id), 3) AS conversion_rate,
  ROUND(AVG(p.payment_value), 2) AS avg_order_value,
  ROUND(AVG(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_purchase_timestamp, DAY)), 2) AS avg_delivery_days,
  ROUND(AVG(r.review_score), 2) AS avg_review_score,
  ROUND(COUNT(DISTINCT r.review_id) * 1.0 / COUNT(DISTINCT o.order_id), 3) AS review_rate
FROM
  `ab-testing-analytics.marketplace_ab_test.orders_with_groups` og
JOIN
  `ab-testing-analytics.marketplace_ab_test.orders` o ON og.order_id = o.order_id
LEFT JOIN
  `ab-testing-analytics.marketplace_ab_test.payments` p ON o.order_id = p.order_id
LEFT JOIN
  `ab-testing-analytics.marketplace_ab_test.reviews` r ON o.order_id = r.order_id
GROUP BY
  og.ab_group;
