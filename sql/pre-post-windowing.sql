-- Calculate pre- and post-rollout KPIs for each A/B group using customer feature exposure dates
create or replace table `ab-testing-analytics.marketplace_ab_test.kpis_pre_post_rollout` as
with selected_fields as (
select o.order_id,
       o.customer_id,
       o.order_purchase_timestamp,
       o.order_status,
       p.payment_value,
       r.review_score,
       cr.ab_group,
       cr.feature_exposure_date,
       case
           when DATE(o.order_purchase_timestamp) < cr.feature_exposure_date then 'PRE'
           else 'POST'
       end as period
    from `ab-testing-analytics.marketplace_ab_test.orders` o
          join `ab-testing-analytics.marketplace_ab_test.customer_rollout` cr
               on o.customer_id = cr.customer_id
          left join `ab-testing-analytics.marketplace_ab_test.payments` p
                    on o.order_id = p.order_id
          left join `ab-testing-analytics.marketplace_ab_test.reviews` r
                    on o.order_id = r.order_id
    where o.order_status is not null
)

select
    ab_group,
    period,
    COUNT(distinct order_id) as total_orders,
    COUNTIF(order_status = 'delivered') as delivered_orders,
    ROUND(COUNTIF(order_status = 'delivered') * 1.0 / COUNT(distinct order_id), 3) as conversion_rate,
    ROUND(AVG(payment_value), 2) as avg_order_value,
    ROUND(AVG(review_score), 2) as avg_review_score
from selected_fields
group by ab_group, period
order by ab_group, period;

