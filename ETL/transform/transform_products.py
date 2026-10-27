import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


# Define the input and output CSV paths.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"


def transform_products():
    """Clean and validate product records."""

    cleaned_products = []
    skipped_records = 0

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Remove unnecessary spaces from text fields.
            for column in row:
                if isinstance(row[column], str):
                    row[column] = row[column].strip()

            # Skip records with missing required values.
            if (
                not row["product_id"]
                or not row["product_name"]
                or not row["category_name"]
            ):
                skipped_records += 1
                continue

            # Validate product price and stock quantity.
            try:
                price = Decimal(row["price"])
                stock = int(row["stock_quantity"])

                if not price.is_finite() or price <= 0 or stock < 0:
                    skipped_records += 1
                    continue

            except (InvalidOperation, ValueError, TypeError):
                skipped_records += 1
                continue

            # Standardize product and category names.
            row["product_name"] = " ".join(row["product_name"].split())
            row["category_name"] = " ".join(row["category_name"].split()).title()

            cleaned_products.append(row)

    # Save the validated products to a new CSV file.
    columns = [
        "product_id",
        "product_name",
        "description",
        "price",
        "stock_quantity",
        "category_name",
        "created_at",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(cleaned_products)

    print(f"Input records processed: {len(cleaned_products) + skipped_records}")
    print(f"Valid products: {len(cleaned_products)}")
    print(f"Skipped records: {skipped_records}")
    print(f"Cleaned data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform_products()