# File: scripts/run_ab_queries.py
# Purpose: Execute all A/B test SQL queries in order using BigQuery API

import os
from google.cloud import bigquery
from settings import get_bigquery_client
from typing import List

SQL_FILES: List[str] = [
    "rollout_assignment.sql",
    "pre_post_windowing.sql",
    "assign_ab_groups.sql",
    "orders_with_ab_groups.sql",
    "conversion_metrics.sql",
    "segment_kpis.sql"
]

SQL_DIR: str = os.path.join(os.path.dirname(__file__), "../sql")

def execute_sql_file(client: bigquery.Client, filepath: str) -> None:
    """
    Execute a SQL script against BigQuery.

    Args:
        client (bigquery.Client): BigQuery client
        filepath (str): Path to the SQL file
    """
    with open(filepath, "r") as file:
        query = file.read()
        print(f"Executing: {os.path.basename(filepath)}")
        job = client.query(query)
        job.result()
        print(f"Completed: {os.path.basename(filepath)}")

def main() -> None:
    client = get_bigquery_client()

    for sql_file in SQL_FILES:
        full_path = os.path.join(SQL_DIR, sql_file)
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            continue
        try:
            execute_sql_file(client, full_path)
        except Exception as e:
            print(f"Error executing {sql_file}: {e}")

if __name__ == "__main__":
    main()
