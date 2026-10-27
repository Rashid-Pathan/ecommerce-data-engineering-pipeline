import os

import psycopg


def extract_products():
    """Extract product records with category details from PostgreSQL."""

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.environ["PGPASSWORD"],
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.product_id,
                    p.product_name,
                    p.description,
                    p.price,
                    p.stock_quantity,
                    c.category_name,
                    p.created_at
                FROM products AS p
                LEFT JOIN categories AS c
                    ON p.category_id = c.category_id
                ORDER BY p.product_id;
            """)

            products = cur.fetchall()

    return products


if __name__ == "__main__":
    products = extract_products()

    print(f"Successfully extracted {len(products)} products.")

    for product in products:
        print(product)