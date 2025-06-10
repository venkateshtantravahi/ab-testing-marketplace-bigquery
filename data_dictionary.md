# Data Dictionary — Olist E-commerce Dataset for A/B Testing

## Overview: BigQuery Schema Behavior

In traditional relational databases (like PostgreSQL or MySQL), we define and enforce relationships using **primary keys** and **foreign keys**. However, in **Google BigQuery**, these constraints are:

- **Not enforced at the database level**
- **Handled logically by the engineer**
- **Modeled via consistent column naming and joins**

This design choice enables BigQuery to prioritize **analytical performance** and **scalability** over transactional integrity.

**Therefore**, all relationships in this dataset are defined **logically**, not physically enforced.

---

## Logical Table Relationships (Entity Diagram View)

![Data Relationship](assets/OlistRelationship.png)

| Child Table             | Join Field                  | Parent Table         | Description |
|------------------------|-----------------------------|----------------------|-------------|
| `orders`               | `customer_id`               | `customers`          | Each order belongs to a customer |
| `order_items`          | `order_id`                  | `orders`             | Each order has 1 or more items |
| `order_items`          | `product_id`                | `products`           | Items refer to a product |
| `order_items`          | `seller_id`                 | `sellers`            | Items are sold by a seller |
| `payments`             | `order_id`                  | `orders`             | Orders have one or more payments |
| `reviews`              | `order_id`                  | `orders`             | Orders can be reviewed |
| `customers`            | `customer_zip_code_prefix`  | `geolocation`        | Customers live in a geolocation |
| `sellers`              | `seller_zip_code_prefix`    | `geolocation`        | Sellers are located in a geolocation |

> All join fields are logically compatible by design. No enforced constraints are needed for BigQuery usage.

---

## Table-by-Table Field Descriptions

### `orders`
| Column                         | Type       | Description |
|-------------------------------|------------|-------------|
| `order_id`                    | STRING     | Unique identifier for an order |
| `customer_id`                 | STRING     | Customer placing the order |
| `order_status`                | STRING     | Status (delivered, shipped, etc.) |
| `order_purchase_timestamp`    | TIMESTAMP  | When the order was placed |
| `order_approved_at`           | TIMESTAMP  | When payment was approved |
| `order_delivered_carrier_date`| TIMESTAMP  | Handed to carrier |
| `order_delivered_customer_date`| TIMESTAMP | Delivered to customer |
| `order_estimated_delivery_date`| TIMESTAMP | Estimated delivery |

---

### `order_items`
| Column             | Type     | Description |
|--------------------|----------|-------------|
| `order_id`        | STRING   | Refers to `orders` |
| `order_item_id`   | INT64    | Line item number within an order |
| `product_id`      | STRING   | Refers to `products` |
| `seller_id`       | STRING   | Refers to `sellers` |
| `shipping_limit_date` | TIMESTAMP | Shipping deadline |
| `price`           | FLOAT64  | Price of the item |
| `freight_value`   | FLOAT64  | Shipping cost |

---

### `payments`
| Column              | Type     | Description |
|---------------------|----------|-------------|
| `order_id`         | STRING   | Refers to `orders` |
| `payment_sequential`| INT64   | Payment sequence for the order |
| `payment_type`     | STRING   | Method (credit card, boleto, etc.) |
| `payment_installments` | INT64 | Number of installments |
| `payment_value`    | FLOAT64  | Payment amount |

---

### `reviews`
| Column                   | Type       | Description |
|--------------------------|------------|-------------|
| `review_id`             | STRING     | Unique review ID |
| `order_id`              | STRING     | Refers to `orders` |
| `review_score`          | INT64      | 1–5 rating |
| `review_comment_title`  | STRING     | Optional title |
| `review_comment_message`| STRING     | Optional feedback |
| `review_creation_date`  | TIMESTAMP  | When review was written |
| `review_answer_timestamp`| TIMESTAMP | When seller replied (if any) |

---

### `customers`
| Column                    | Type     | Description |
|---------------------------|----------|-------------|
| `customer_id`            | STRING   | Customer's ID |
| `customer_unique_id`     | STRING   | Common across re-orders |
| `customer_zip_code_prefix`| STRING  | Zip code segment |
| `customer_city`          | STRING   | City name |
| `customer_state`         | STRING   | State code (e.g., SP, RJ) |

---

### `sellers`
| Column                   | Type     | Description |
|--------------------------|----------|-------------|
| `seller_id`             | STRING   | Unique seller ID |
| `seller_zip_code_prefix`| STRING   | Zip prefix |
| `seller_city`           | STRING   | City |
| `seller_state`          | STRING   | State |

---

### `products`
| Column                    | Type     | Description |
|---------------------------|----------|-------------|
| `product_id`             | STRING   | Unique product ID |
| `product_category_name`  | STRING   | Category |
| `product_name_length`    | INT64    | Length of name |
| `product_description_length`| INT64 | Length of description |
| `product_photos_qty`     | INT64    | Number of photos |
| `product_weight_g`       | FLOAT64  | Weight in grams |
| `product_length_cm`      | FLOAT64  | Length |
| `product_height_cm`      | FLOAT64  | Height |
| `product_width_cm`       | FLOAT64  | Width |

---

### `geolocation`
| Column                    | Type     | Description |
|---------------------------|----------|-------------|
| `geolocation_zip_code_prefix` | STRING | Zip prefix (used for joins) |
| `geolocation_lat`         | FLOAT64  | Latitude |
| `geolocation_lng`         | FLOAT64  | Longitude |
| `geolocation_city`        | STRING   | City |
| `geolocation_state`       | STRING   | State |

---

## Summary

While BigQuery does not enforce traditional constraints like primary or foreign keys, this dataset is designed with **clear relational intent**. Analysts and engineers can reliably build joins, aggregations, and A/B test logic using the field mappings outlined above.

➡ For schema definitions, see [`/sql/*.sql`](../sql)  
➡ For data loading logic, see [`/scripts/`](../scripts)

---
