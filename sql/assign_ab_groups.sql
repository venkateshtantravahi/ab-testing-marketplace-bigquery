-- Assign customers to A/B test groups (50/50) based on customer_id fingerprint
create or replace table `ab-testing-analytics.marketplace_ab_test.customer_groups` as
    select
        customer_id,
        IF(MOD(ABS(FARM_FINGERPRINT(customer_id)), 2) = 0, 'A', 'B') as ab_group
    from
        `ab-testing-analytics.marketplace_ab_test.customers`;