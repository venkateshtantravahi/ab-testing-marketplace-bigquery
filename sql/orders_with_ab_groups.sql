-- Enrich order table with A/B group info
create or replace table `ab-testing-analytics.marketplace_ab_test.orders_with_groups` as
    select
        o.*,
        cg.ab_group
    from
        `ab-testing-analytics.marketplace_ab_test.orders` o
    join
        `ab-testing-analytics.marketplace_ab_test.customer_groups` cg
    on
        o.customer_id = cg.customer_id;