# File: scripts/create_bigquery_tables.py
# Purpose: Create dataset and tables in BigQuery using schema SQL files

import os
from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from settings import get_bigquery_client, PROJECT_ID, BQ_DATASET_NAME

SQL_DIR: str = os.path.join(os.path.dirname(__file__), "../sql")


def ensure_dataset(client: bigquery.Client) -> None:
    """
    Creates the dataset in BigQuery if it doesn't exist.

    Args:
        client (bigquery.Client): BigQuery client instance.
    """
    dataset_ref = Dataset(f"{PROJECT_ID}.{BQ_DATASET_NAME}")
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset already exists: {BQ_DATASET_NAME}")
    except NotFound:
        client.create_dataset(dataset_ref)
        print(f"Created dataset: {BQ_DATASET_NAME}")


def execute_sql(client: bigquery.Client, sql_dir: str) -> None:
    """
    Executes all .sql files in the given directory to create BigQuery tables.

    Args:
        client (bigquery.Client): BigQuery client instance.
        sql_dir (str): Path to the directory containing .sql files.
    """
    for filename in sorted(os.listdir(sql_dir)):
        if filename.endswith(".sql"):
            file_path = os.path.join(sql_dir, filename)
            with open(file_path, "r") as sql_file:
                query = sql_file.read()
            print(f"Executing: {filename}")
            try:
                client.query(query).result()
                print(f"Success: {filename}\n")
            except Exception as e:
                print(f"Failed: {filename} with error: {e}\n")


def main() -> None:
    """Main execution entrypoint to set up BigQuery tables."""
    print("Creating BigQuery tables...")
    client = get_bigquery_client()
    ensure_dataset(client)
    execute_sql(client, SQL_DIR)
    print("All tables created.")


if __name__ == "__main__":
    main()
