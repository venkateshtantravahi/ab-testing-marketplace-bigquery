-- SQL schema definitions for Olist E-commerce Dataset
-- Target Dataset: ab-testing-analytics.marketplace_ab_test

-- 1. olist_orders_dataset
create or replace table `ab-testing-analytics.marketplace_ab_test.orders` (
       order_id string,
       customer_id string,
       order_status string,
       order_purchase_timestamp timestamp,
       order_approved_at TIMESTAMP,
       order_delivered_carrier_date TIMESTAMP,
       order_delivered_customer_date TIMESTAMP,
       order_estimated_delivery_date TIMESTAMP
);

-- 2. olist_order_items_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.order_items` (
    order_id STRING,
    order_item_id INT64,
    product_id STRING,
    seller_id STRING,
    shipping_limit_date TIMESTAMP,
    price FLOAT64,
    freight_value FLOAT64
);

-- 3. olist_order_payments_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.payments` (
    order_id STRING,
    payment_sequential INT64,
    payment_type STRING,
    payment_installments INT64,
    payment_value FLOAT64
);

-- 4. olist_order_reviews_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.reviews` (
    review_id STRING,
    order_id STRING,
    review_score INT64,
    review_comment_title STRING,
    review_comment_message STRING,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

-- 5. olist_order_customer_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.customers` (
    customer_id STRING,
    customer_unique_id STRING,
    customer_zip_code_prefix STRING,
    customer_city STRING,
    customer_state STRING
);

-- 6. olist_sellers_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.sellers` (
    seller_id STRING,
    seller_zip_code_prefix STRING,
    seller_city STRING,
    seller_state STRING
);

-- 7. olist_products_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.products` (
    product_id STRING,
    product_category_name STRING,
    product_name_length INT64,
    product_description_length INT64,
    product_photos_qty INT64,
    product_weight_g FLOAT64,
    product_length_cm FLOAT64,
    product_height_cm FLOAT64,
    product_width_cm FLOAT64
);

-- 8. olist_geolocation_dataset
CREATE OR REPLACE TABLE `ab-testing-analytics.marketplace_ab_test.geolocation` (
    geolocation_zip_code_prefix STRING,
    geolocation_lat FLOAT64,
    geolocation_lng FLOAT64,
    geolocation_city STRING,
    geolocation_state STRING
);