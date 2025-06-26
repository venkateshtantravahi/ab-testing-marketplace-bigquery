# File: scripts/simulate_events.py
# Purpose: Generate synthetic event logs to simulate real-time A/B test tracking

import pandas as pd
import numpy as np
from datetime import timedelta
from settings import get_bigquery_client


def simulate_event_row(row: pd.Series) -> list[dict]:
    """
    Simulates event rows for an individual order.

    Args:
        row (pd.Series): A row containing order and customer details.

    Returns:
        list[dict]: A list of event dictionaries.
    """
    events = []
    base_time = pd.to_datetime(row["order_purchase_timestamp"])

    # Order placed event
    events.append({
        "customer_id": row["customer_id"],
        "order_id": row["order_id"],
        "event_type": "order_placed",
        "event_timestamp": base_time,
        "ab_group": row["ab_group"]
    })

    # Payment event
    if not pd.isna(row["payment_value"]):
        events.append({
            "customer_id": row["customer_id"],
            "order_id": row["order_id"],
            "event_type": "payment_success",
            "event_timestamp": base_time + timedelta(minutes=np.random.randint(5, 120)),
            "ab_group": row["ab_group"]
        })

    # Review event
    if not pd.isna(row["review_score"]):
        events.append({
            "customer_id": row["customer_id"],
            "order_id": row["order_id"],
            "event_type": f"review_{int(row['review_score'])}star",
            "event_timestamp": base_time + timedelta(days=np.random.randint(5, 20)),
            "ab_group": row["ab_group"]
        })

    return events


def generate_events() -> None:
    """
    Loads order data from BigQuery, simulates event streams, and writes to CSV.
    """
    client = get_bigquery_client()

    query = """
    SELECT
      o.order_id,
      o.customer_id,
      o.order_purchase_timestamp,
      p.payment_value,
      r.review_score,
      cr.ab_group,
      cr.feature_exposure_date
    FROM `ab-testing-analytics.marketplace_ab_test.orders` o
    JOIN `ab-testing-analytics.marketplace_ab_test.customer_rollout` cr
      ON o.customer_id = cr.customer_id
    LEFT JOIN `ab-testing-analytics.marketplace_ab_test.payments` p
      ON o.order_id = p.order_id
    LEFT JOIN `ab-testing-analytics.marketplace_ab_test.reviews` r
      ON o.order_id = r.order_id
    """
    df = client.query(query).to_dataframe()

    all_events = []
    for _, row in df.iterrows():
        all_events.extend(simulate_event_row(row))

    events_df = pd.DataFrame(all_events)
    events_df.to_csv("../data/synthetic_events.csv", index=False)
    print("Synthetic event log saved to data/synthetic_events.csv")


if __name__ == "__main__":
    generate_events()