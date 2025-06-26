# File: scripts/load_to_bigquery.py
# Purpose: Upload local CSV files to BigQuery tables (assumes table schemas already exist)

import os
from typing import Dict
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from settings import get_bigquery_client, PROJECT_ID, BQ_DATASET_NAME

DATA_DIR: str = "../data"
CSV_TO_TABLE_MAP: Dict[str, str] = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
}

def load_csv_to_table(client: bigquery.Client, file_path: str, table_id: str) -> None:
    """
    Load a local CSV file into an existing BigQuery table.

    Args:
        client (bigquery.Client): BigQuery client instance
        file_path (str): Path to the CSV file
        table_id (str): Fully qualified BigQuery table ID
    """
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        field_delimiter=",",
        allow_quoted_newlines=True,
    )

    print(f"Loading data from {file_path} -> {table_id}")
    try:
        with open(file_path, "rb") as csv_file:
            job = client.load_table_from_file(csv_file, table_id, job_config=job_config)
        job.result()
        print(f"Loaded {job.output_rows} rows into `{table_id}`")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except NotFound:
        print(f"Table not found: {table_id}")
    except Exception as ex:
        print(f"Failed to load {table_id}: {ex}")

def main() -> None:
    """
    Iterate over CSV files and load them into corresponding BigQuery tables.
    """
    client = get_bigquery_client()

    if not PROJECT_ID or not BQ_DATASET_NAME:
        raise ValueError("Missing PROJECT_ID or BQ_DATASET_NAME from settings.")

    for csv_file, table_name in CSV_TO_TABLE_MAP.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        table_id = f"{PROJECT_ID}.{BQ_DATASET_NAME}.{table_name}"
        load_csv_to_table(client, file_path, table_id)

if __name__ == "__main__":
    main()
