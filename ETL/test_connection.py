
import psycopg

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=input("Enter PostgreSQL password: ")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM customers;")
            result = cur.fetchone()

            print("Database connection successful!")
            print("Total customers:", result[0])

except Exception as e:
    print("Connection failed:", e)
