import os
from typing import Dict
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
DATASET_ID: str = os.getenv("BQ_DATASET_NAME", "")
DATA_DIR: str = "data"

# Mapping: filename → table name
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


def get_bigquery_client() -> bigquery.Client:
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID is not set in the environment.")
    return bigquery.Client(project=PROJECT_ID)


def load_csv_to_table(
    client: bigquery.Client, file_path: str, table_name: str
) -> None:
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
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
        print(f"Loaded {job.output_rows} rows into `{table_name}`")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except NotFound as nf:
        print(f" Table {table_name} not found.")
    except Exception as ex:
        print(f" Failed to load table {table_name}: {ex}")


def main():
    client = get_bigquery_client()
    print("Loading CSV to BigQuery...")

    for csv_file, table_name in CSV_TO_TABLE_MAP.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        load_csv_to_table(client, file_path, table_name)

    print("Done.")


if __name__ == "__main__":
    main()