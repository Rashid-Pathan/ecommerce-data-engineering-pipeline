
import os

import psycopg


def check_data_quality():
    """Validate customer data in the staging table."""

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
                    COUNT(*) AS total_customers,
                    COUNT(DISTINCT email) AS unique_emails,
                    COUNT(*) FILTER (
                        WHERE email IS NULL OR TRIM(email) = ''
                    ) AS missing_emails,
                    COUNT(*) FILTER (
                        WHERE first_name IS NULL
                           OR TRIM(first_name) = ''
                           OR last_name IS NULL
                           OR TRIM(last_name) = ''
                    ) AS missing_names
                FROM staging_customers;
            """)

            total, unique_emails, missing_emails, missing_names = cur.fetchone()

            cur.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT LOWER(TRIM(email))
                    FROM staging_customers
                    WHERE email IS NOT NULL
                      AND TRIM(email) <> ''
                    GROUP BY LOWER(TRIM(email))
                    HAVING COUNT(*) > 1
                ) AS duplicates;
            """)

            duplicate_emails = cur.fetchone()[0]

    print("\n--- Customer Data Quality Report ---")
    print(f"Total customers: {total}")
    print(f"Unique email values: {unique_emails}")
    print(f"Missing emails: {missing_emails}")
    print(f"Duplicate email groups: {duplicate_emails}")
    print(f"Records with missing names: {missing_names}")

    passed = (
        missing_emails == 0
        and duplicate_emails == 0
        and missing_names == 0
    )

    if passed:
        print("\nData quality check PASSED.")
    else:
        print("\nData quality check FAILED.")


if __name__ == "__main__":
    check_data_quality()
