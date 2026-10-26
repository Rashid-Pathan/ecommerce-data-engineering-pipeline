
import csv
from pathlib import Path

from extract_customers import extract_customers


# Define the output CSV path in the processed data folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "customers.csv"

# Make sure the output directory exists.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Extract customer records from PostgreSQL.
customers = extract_customers()

# Save the extracted records to a CSV file.
columns = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "city",
    "country",
    "created_at",
]

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)

    for customer in customers:
        writer.writerow(customer)

print(f"Exported {len(customers)} customers to: {OUTPUT_FILE}")
