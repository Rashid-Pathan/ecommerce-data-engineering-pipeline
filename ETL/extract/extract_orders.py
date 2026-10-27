import os

import psycopg


def extract_orders():
    """Extract order records with customer details from PostgreSQL."""

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
                    o.order_id,
                    o.customer_id,
                    o.order_date,
                    o.status,
                    o.total_amount
                FROM orders AS o
                ORDER BY o.order_id;
            """)

            orders = cur.fetchall()

    return orders


if __name__ == "__main__":
    orders = extract_orders()

    print(f"Successfully extracted {len(orders)} orders.")

    for order in orders:
        print(order)