import os
import psycopg


def extract_order_items():
    """Extract order item records from PostgreSQL."""

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
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                FROM order_items
                ORDER BY order_item_id;
            """)

            order_items = cur.fetchall()

    return order_items


if __name__ == "__main__":
    order_items = extract_order_items()

    print(f"Successfully extracted {len(order_items)} order items.")

    for item in order_items:
        print(item)