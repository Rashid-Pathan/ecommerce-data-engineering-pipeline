
import psycopg


def extract_customers():
    """Extract customer records from PostgreSQL."""

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=input("Enter PostgreSQL password: ")
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    customer_id,
                    first_name,
                    last_name,
                    email,
                    city,
                    country,
                    created_at
                FROM customers
                ORDER BY customer_id;
            """)

            customers = cur.fetchall()

    return customers


if __name__ == "__main__":
    data = extract_customers()

    print(f"Successfully extracted {len(data)} customers.")

    for customer in data:
        print(customer)
