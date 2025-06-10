# Hypothesis Plan for A/B Testing — Olist Marketplace

## Project Objective
To evaluate the impact of introducing a new feature or change in the Olist marketplace platform using a simulated A/B testing framework. This analysis aims to assess how the change affects user behavior, customer satisfaction, operational efficiency, and monetization.

---

## Background Context (from EDA)

Based on comprehensive exploratory data analysis (see `eda_orders.ipynb`), we uncovered several behavioral and business-relevant insights:

- **Order Spike**: A sharp spike in orders during Q4 2017 followed by a consistent pattern (suggesting a peak campaign or anomaly).
- **High-selling categories**: Items like `cama_mesa_banho` and `beleza_saude` dominate product sales.
- **Payment behavior**: Most transactions are below $200, with a long-tail distribution up to $500.
- **Geographic influence**: States like SP, RJ, and MG dominate order volume and seller base.
- **Freight cost varies** widely across seller states, potentially influencing delivery KPIs.
- **Review score skewed positively**, with a majority being 5-star.

---

## Multi-Hypothesis Design

Below are the **hypotheses** crafted from domain knowledge and EDA observations:

### Hypothesis 1: Conversion Rate Impact
> *The new feature improves conversion rate (i.e., more orders per user in Group B compared to Group A).*
- Rationale: Positive user experience may increase purchase likelihood.
- Metric: Conversion rate = Delivered Orders / Total Orders

### Hypothesis 2: Average Order Value (AOV) Uplift
> *Group B exhibits a higher average payment value per order.*
- Rationale: If feature boosts trust (e.g., better filters), users may spend more.
- Metric: `AVG(payment_value)`

### Hypothesis 3: Delivery Efficiency
> *Group B sees faster average delivery time.*
- Rationale: Indirect impact if feature leads to better product sorting or seller preference.
- Metric: `AVG(order_delivered_customer_date - order_purchase_timestamp)`

### Hypothesis 4: User Satisfaction
> *Group B receives higher average review scores.*
- Rationale: Better experience may result in more positive feedback.
- Metric: `AVG(review_score)`

### Hypothesis 5: Review Engagement Rate
> *Group B leaves more reviews per order.*
- Rationale: Higher engagement could indicate better UX.
- Metric: `COUNT(reviews) / COUNT(orders)`

---

## Metrics Summary Table

| Hypothesis # | KPI                          | Description                                |
|--------------|------------------------------|--------------------------------------------|
| H1           | Conversion Rate              | Delivered orders / Total orders            |
| H2           | Avg. Order Value (AOV)       | Mean of payment values                     |
| H3           | Delivery Time                | Mean delivery duration in days             |
| H4           | Avg. Review Score            | Mean of review scores (1–5)                |
| H5           | Review Rate                  | Ratio of reviews to orders                 |

---

## Testing Plan Outline

- **Randomized Assignment**: Customers will be randomly assigned to Groups A & B using `FARM_FINGERPRINT()`
- **Stratified Matching** : Match A/B groups by `customer_state` or order history frequency
- **Group-Level Aggregation**: KPIs calculated per group
- **Statistical Tests**: t-tests for means, chi-square for proportions where applicable
- **Interpretation**: Include confidence intervals and p-values for all tests

---

## References

- EDA visualizations and raw patterns can be found in: [`notebooks/eda_orders.ipynb`](notebooks/ExploratoryDataAnalysis.ipynb)
- Data source details and schema: [`data_dictionary.md`](data_dictionary.md)
- This file should be referenced in the main [`README.md`](README.md) as the A/B testing design documentation.
