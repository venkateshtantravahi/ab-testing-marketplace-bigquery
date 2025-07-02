# A/B Testing Marketplace Features using BigQuery

A complete, production-grade data science project to simulate and evaluate the rollout of new product features in a marketplace setting using A/B testing principles. This project leverages **Google BigQuery**, **Polars**, **Python**, and **Tableau/Matplotlib** to build an end-to-end experiment analysis workflow.

---

## Project Overview

This project answers a key question:

> **"How do we measure the true impact of a new feature on user behavior in a marketplace?"**

We simulate a real-world A/B testing scenario where a new feature (like price matching or advanced filters) is rolled out to part of a user base. The experiment is evaluated by comparing core business KPIs such as:

- Conversion Rate
- Average Order Value
- Review Score

---

## Why A/B Testing?

A/B Testing is the **gold standard** for causal inference in product experimentation. It helps us:

- Quantify impact of product changes
- Minimize risk from assumptions or bias
- Make statistically sound decisions based on real behavior

### Real-Life Analogy
Imagine you're testing two versions of a product page: one with a price badge and one without. By randomly assigning users to version A or B, you can see which version performs better in **actual conversion**, not just in theory.

This project simulates that logic — at a marketplace level.

---

## Dataset Used

We use the [Olist E-commerce Public Dataset (Brazil)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle, which includes:

- Orders, customers, reviews, payments
- Products, sellers, categories

This allows for deep buyer-seller behavior modeling and realistic simulation of feature testing.

---

## Project Structure

```bash
ab-testing-marketplace-bigquery/
├── data/                    # CSV data from Olist (not included in repo)
├── notebooks/              # Jupyter Notebooks for EDA & analysis
├── sql/                    # SQL queries for BigQuery table creation and KPIs
├── scripts/                # Python scripts for automation and BigQuery interaction
├── dashboard/              # (Optional) Tableau workbooks or config files
├── reports/                # Visualizations and exported KPIs for sharing
├── .env                    # Environment file (not committed)
├── requirements.txt        # Python dependencies
├── README.md               # You are here 
└── LICENSE
```

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/ab-testing-marketplace-bigquery.git
cd ab-testing-marketplace-bigquery
```

### 2. Install Requirements
Create and activate a virtual environment (recommended):
```bash
python3 -m venv ab-testing
source ab-testing/bin/activate
pip install -r requirements.txt
```

### 3. Configure `.env`
Create a `.env` file with your GCP credentials:

```dotenv
GCP_PROJECT_ID=your-project-id
BQ_DATASET_NAME=marketplace_ab_test
```

> **NOTE:** `.env` is excluded from version control. You must create it locally.

### 4. Upload Data to BigQuery
Ensure BigQuery dataset and tables are created:
```bash
python scripts/create_bigquery_tables.py
python scripts/load_to_bigquery.py
```

Then run all A/B queries:
```bash
python scripts/run_ab_queries.py
```

---

## Analysis Overview

### KPI Computation
All metrics are computed using SQL and stored in BigQuery:
- Conversion rate (delivered orders / total orders)
- Average payment value
- Average review score

### Statistical Testing
The analysis includes:
- `Z-Test` for conversion rate difference
- `Welch’s T-Test` for average order value
- Descriptive comparison for review score

### Interpretation
Visual and textual insights are provided to interpret:
- KPI trends between groups
- Statistically significant shifts

---

## Extending This Project

Here’s how you can go further:
- Add time-window based causal inference (e.g., CausalImpact, CUSUM)
- Expand to include segmentation analysis (state, product category)
- Integrate with Looker Studio or Tableau dashboards
- Use raw logs to simulate real-time experimentation

---

## Contributing

We welcome contributions!
1. Fork the repo
2. Create your feature branch: `git checkout -b my-feature`
3. Commit changes: `git commit -am 'Add awesome feature'`
4. Push to branch: `git push origin my-feature`
5. Open a pull request

---

## Notes on Data & Environment

- `data/` is excluded via `.gitignore`. Download Olist data from Kaggle and place CSVs here.
- `.env` must be created manually for secure GCP credentials.

---

## License

This project is licensed under the MIT [License](LICENSE).

---

## Acknowledgments

- [Olist Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Google BigQuery
- Polars & Matplotlib for analysis
