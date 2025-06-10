import os
from typing import Optional

from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from dotenv import load_dotenv

#load environment variables
load_dotenv()

PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID")
DATASET_ID: Optional[str] = os.getenv("BQ_DATASET_NAME")
SQL_DIR: str = "sql"

def get_client() -> bigquery.Client:
    """Initializes the BigQuery client using the provided project ID."""
    if PROJECT_ID is None:
        raise ValueError("GCP_PROJECT_ID is not set in the environment.")
    return bigquery.Client(project=PROJECT_ID)


def ensure_dataset(client: bigquery.Client) -> None:
    """Creates the dataset if it doesn't exist."""
    dataset_ref = Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists.")
    except NotFound:
        client.create_dataset(dataset_ref)
        print(f"Created dataset {DATASET_ID}.")


def execute_sql(client: bigquery.Client, sql_dir: str) -> None:
    """Executes the SQL queries against the BigQuery dataset."""
    for filename in sorted(os.listdir(sql_dir)):
        if filename.endswith(".sql"):
            file_path = os.path.join(sql_dir, filename)
            with open(file_path, "r") as sql_file:
                query = sql_file.read()
            print(f"Executing SQL query: {query}")
            try:
                client.query(query).result()
                print(f"Successfully executed SQL query: {query}\n")
            except Exception as e:
                print(f"Failed to execute SQL query: {query} with error {e}\n")


def main():
    """Main execution flow for creating dataset and tables."""
    print("Creating BigQuery tables...")
    client = get_client()
    ensure_dataset(client)
    execute_sql(client, SQL_DIR)
    print("Done.")

if __name__ == "__main__":
    main()