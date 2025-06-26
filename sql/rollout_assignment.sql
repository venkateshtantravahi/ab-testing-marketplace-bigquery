-- Assign feature rollout dates to each customer to simulate staged A/B test behavior.

CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.customer_rollout` AS
    SELECT
        customer_id,
        IF(MOD(ABS(FARM_FINGERPRINT(customer_id)), 2) = 0, 'A', 'B') as ab_group,
        CASE
            WHEN MOD(ABS(FARM_FINGERPRINT(customer_id)), 2) = 0 THEN DATE('2017-09-01')
            ELSE DATE('2017-10-01')
        END AS feature_exposure_date
FROM `ab-testing-analytics.marketplace_ab_test.customers`