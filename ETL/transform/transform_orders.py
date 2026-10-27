import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


# Define the input and output CSV paths.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "orders.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "orders_cleaned.csv"

# Define the accepted order statuses.
VALID_STATUSES = {"Pending", "Processing", "Shipped", "Completed", "Cancelled"}


def transform_orders():
    """Validate and clean order records."""

    cleaned_orders = []
    skipped_records = 0

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Remove unnecessary spaces from text fields.
            for column in row:
                if isinstance(row[column], str):
                    row[column] = row[column].strip()

            # Skip records with missing required values.
            if not all(row[field] for field in [
                "order_id",
                "customer_id",
                "order_date",
                "status",
                "total_amount",
            ]):
                skipped_records += 1
                continue

            # Validate IDs and order amount.
            try:
                order_id = int(row["order_id"])
                customer_id = int(row["customer_id"])
                amount = Decimal(row["total_amount"])

                if (
                    order_id <= 0
                    or customer_id <= 0
                    or not amount.is_finite()
                    or amount < 0
                ):
                    skipped_records += 1
                    continue

            except (ValueError, InvalidOperation):
                skipped_records += 1
                continue

            # Standardize and validate order status.
            row["status"] = row["status"].title()

            if row["status"] not in VALID_STATUSES:
                skipped_records += 1
                continue

            cleaned_orders.append(row)

    # Save the validated orders to a new CSV file.
    columns = [
        "order_id",
        "customer_id",
        "order_date",
        "status",
        "total_amount",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(cleaned_orders)

    print(f"Input records processed: {len(cleaned_orders) + skipped_records}")
    print(f"Valid orders: {len(cleaned_orders)}")
    print(f"Skipped records: {skipped_records}")
    print(f"Cleaned data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform_orders()