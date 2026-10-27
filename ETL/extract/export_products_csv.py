import csv
from pathlib import Path

from extract_products import extract_products


# Define the output CSV path in the processed data folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products.csv"

# Create the output directory if it does not exist.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Extract product records from PostgreSQL.
products = extract_products()

# Define CSV column names.
columns = [
    "product_id",
    "product_name",
    "description",
    "price",
    "stock_quantity",
    "category_name",
    "created_at",
]

# Save the extracted products to a CSV file.
with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(products)

print(f"Exported {len(products)} products to: {OUTPUT_FILE}")