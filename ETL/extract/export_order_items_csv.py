import csv
from pathlib import Path
from extract_order_items import extract_order_items


def export_order_items_to_csv():
    """Export extracted order items to a CSV file."""

    order_items = extract_order_items()

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "order_items.csv"

    columns = [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(order_items)

    print(f"Successfully exported {len(order_items)} order items.")
    print(f"File saved at: {output_file}")


if __name__ == "__main__":
    export_order_items_to_csv()