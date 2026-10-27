import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


def transform_order_items():
    """Clean and validate order item records."""

    input_file = Path("data/processed/order_items.csv")
    output_file = Path("data/processed/order_items_cleaned.csv")

    cleaned_items = []
    skipped_rows = 0

    with open(input_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                order_item_id = int(row["order_item_id"])
                order_id = int(row["order_id"])
                product_id = int(row["product_id"])
                quantity = int(row["quantity"])
                unit_price = Decimal(row["unit_price"])

                if (
                    order_item_id <= 0
                    or order_id <= 0
                    or product_id <= 0
                    or quantity <= 0
                    or not unit_price.is_finite()
                    or unit_price < 0
                ):
                    skipped_rows += 1
                    continue

                cleaned_items.append({
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": f"{unit_price:.2f}",
                })

            except (ValueError, InvalidOperation, TypeError):
                skipped_rows += 1

    output_file.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(cleaned_items)

    print(f"Successfully transformed {len(cleaned_items)} order items.")
    print(f"Skipped invalid rows: {skipped_rows}")
    print(f"Cleaned file saved at: {output_file}")


if __name__ == "__main__":
    transform_order_items()