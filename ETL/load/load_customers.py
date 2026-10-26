
import csv
import os
from pathlib import Path

import psycopg


# Locate the cleaned customer CSV file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "customers_cleaned.csv"


def load_customers():
    """Load cleaned customer records into a PostgreSQL staging table."""

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        customers = list(csv.DictReader(file))

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.environ["PGPASSWORD"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging_customers (
                    customer_id INTEGER PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    city VARCHAR(50),
                    country VARCHAR(50),
                    created_at TIMESTAMP
                );
            """)

            for customer in customers:
                cur.execute("""
                    INSERT INTO staging_customers (
                        customer_id,
                        first_name,
                        last_name,
                        email,
                        city,
                        country,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (customer_id) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        email = EXCLUDED.email,
                        city = EXCLUDED.city,
                        country = EXCLUDED.country,
                        created_at = EXCLUDED.created_at;
                """, (
                    int(customer["customer_id"]),
                    customer["first_name"],
                    customer["last_name"],
                    customer["email"],
                    customer["city"] or None,
                    customer["country"],
                    customer["created_at"] or None,
                ))

    print(f"Successfully loaded {len(customers)} customers.")


if __name__ == "__main__":
    load_customers()
