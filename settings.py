# File: src/settings.py
# Purpose: Centralized project settings for environment and BigQuery configuration

import os
from dotenv import load_dotenv
from google.cloud import bigquery
from typing import Literal

# Load environment variables from .env
load_dotenv()

# Define supported environments
env: Literal["dev", "prod"] = os.getenv("ENV", "dev")

# Environment-specific prefixes or configs (extend as needed)
ENV_CONFIG = {
    "dev": {
        "PROJECT_ID": os.getenv("GCP_PROJECT_ID_DEV"),
        "BQ_DATASET_NAME": os.getenv("BQ_DATASET_NAME_DEV"),
    },
    "prod": {
        "PROJECT_ID": os.getenv("GCP_PROJECT_ID_PROD"),
        "BQ_DATASET_NAME": os.getenv("BQ_DATASET_NAME_PROD"),
    },
}

# Fallbacks for direct env usage (if not using ENV-specific keys)
PROJECT_ID: str = ENV_CONFIG.get(env, {}).get("PROJECT_ID") or os.getenv("GCP_PROJECT_ID", "")
BQ_DATASET_NAME: str = ENV_CONFIG.get(env, {}).get("BQ_DATASET_NAME") or os.getenv("BQ_DATASET_NAME", "")
LOCATION: str = os.getenv("BQ_LOCATION", "US")

# Validate critical configs
if not PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID not set for environment: " + env)
if not BQ_DATASET_NAME:
    raise ValueError("BQ_DATASET_NAME not set for environment: " + env)

def get_bigquery_client() -> bigquery.Client:
    """Returns an authenticated BigQuery client instance."""
    return bigquery.Client(project=PROJECT_ID, location=LOCATION)
