
import csv
import os
from pathlib import Path

import psycopg


# Locate the cleaned products CSV file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"


def load_products():
    """Load cleaned product records into PostgreSQL staging."""

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        products = list(csv.DictReader(file))

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.environ["PGPASSWORD"],
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging_products (
                    product_id INTEGER PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price NUMERIC(10, 2) NOT NULL,
                    stock_quantity INTEGER NOT NULL,
                    category_name VARCHAR(50),
                    created_at TIMESTAMP
                );
            """)

            for product in products:
                cur.execute("""
                    INSERT INTO staging_products (
                        product_id,
                        product_name,
                        description,
                        price,
                        stock_quantity,
                        category_name,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (product_id) DO UPDATE SET
                        product_name = EXCLUDED.product_name,
                        description = EXCLUDED.description,
                        price = EXCLUDED.price,
                        stock_quantity = EXCLUDED.stock_quantity,
                        category_name = EXCLUDED.category_name,
                        created_at = EXCLUDED.created_at;
                """, (
                    int(product["product_id"]),
                    product["product_name"],
                    product["description"] or None,
                    product["price"],
                    int(product["stock_quantity"]),
                    product["category_name"] or None,
                    product["created_at"] or None,
                ))

    print(f"Successfully loaded {len(products)} products.")


if __name__ == "__main__":
    load_products()
