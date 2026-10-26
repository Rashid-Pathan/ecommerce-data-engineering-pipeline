
import csv
from pathlib import Path


# Define the input and output CSV paths.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "customers.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "customers_cleaned.csv"


def transform_customers():
    """Clean customer data and save the transformed records."""

    cleaned_customers = []

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Remove unnecessary spaces from text fields.
            for column in row:
                if isinstance(row[column], str):
                    row[column] = row[column].strip()

            # Skip records with missing customer IDs or emails.
            if not row["customer_id"] or not row["email"]:
                continue

            # Standardize email addresses.
            row["email"] = row["email"].lower()

            cleaned_customers.append(row)

    # Write the cleaned records to a new CSV file.
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "first_name",
                "last_name",
                "email",
                "city",
                "country",
                "created_at",
            ],
        )
        writer.writeheader()
        writer.writerows(cleaned_customers)

    print(f"Input records processed: {len(cleaned_customers)}")
    print(f"Cleaned data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform_customers()
