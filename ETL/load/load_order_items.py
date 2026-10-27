import csv
import os
from pathlib import Path

import psycopg


def load_order_items():
    """Load cleaned order items into the PostgreSQL staging table."""

    input_file = Path("data/processed/order_items_cleaned.csv")

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.environ["PGPASSWORD"],
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging_order_items (
                    order_item_id INTEGER PRIMARY KEY,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price NUMERIC(10, 2) NOT NULL
                );
            """)

            with open(input_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cur.execute("""
                        INSERT INTO staging_order_items (
                            order_item_id,
                            order_id,
                            product_id,
                            quantity,
                            unit_price
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (order_item_id)
                        DO UPDATE SET
                            order_id = EXCLUDED.order_id,
                            product_id = EXCLUDED.product_id,
                            quantity = EXCLUDED.quantity,
                            unit_price = EXCLUDED.unit_price;
                    """, (
                        int(row["order_item_id"]),
                        int(row["order_id"]),
                        int(row["product_id"]),
                        int(row["quantity"]),
                        row["unit_price"],
                    ))

            cur.execute("SELECT COUNT(*) FROM staging_order_items;")
            total_rows = cur.fetchone()[0]

    print(f"Successfully loaded order items.")
    print(f"Total records in staging_order_items: {total_rows}")


if __name__ == "__main__":
    load_order_items()