import csv
from pathlib import Path

from extract_orders import extract_orders


# Define the output CSV path.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "orders.csv"

# Create the output directory if it does not exist.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Extract order records from PostgreSQL.
orders = extract_orders()

# Define CSV column names.
columns = [
    "order_id",
    "customer_id",
    "order_date",
    "status",
    "total_amount",
]

# Export the orders to CSV.
with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(orders)

print(f"Exported {len(orders)} orders to: {OUTPUT_FILE}")