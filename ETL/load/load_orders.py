import csv
import os
from pathlib import Path

import psycopg


# Locate the cleaned orders CSV file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "orders_cleaned.csv"


def load_orders():
    """Load cleaned order records into a PostgreSQL staging table."""

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        orders = list(csv.DictReader(file))

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.environ["PGPASSWORD"],
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging_orders (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    order_date TIMESTAMP NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    total_amount NUMERIC(10, 2) NOT NULL
                );
            """)

            for order in orders:
                cur.execute("""
                    INSERT INTO staging_orders (
                        order_id,
                        customer_id,
                        order_date,
                        status,
                        total_amount
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (order_id) DO UPDATE SET
                        customer_id = EXCLUDED.customer_id,
                        order_date = EXCLUDED.order_date,
                        status = EXCLUDED.status,
                        total_amount = EXCLUDED.total_amount;
                """, (
                    int(order["order_id"]),
                    int(order["customer_id"]),
                    order["order_date"],
                    order["status"],
                    order["total_amount"],
                ))

    print(f"Successfully loaded {len(orders)} orders.")


if __name__ == "__main__":
    load_orders()