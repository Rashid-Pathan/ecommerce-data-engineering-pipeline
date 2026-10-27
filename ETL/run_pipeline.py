import subprocess
import sys
from pathlib import Path


# Find the project and ETL directories.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ETL_DIR = Path(__file__).resolve().parent


def run_step(step_name, script_path):
    """Run one ETL step and stop if it fails."""

    print(f"\n{'=' * 50}")
    print(f"Starting: {step_name}")
    print("=" * 50)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print(f"Completed: {step_name}")


def main():
    """Execute the complete customer ETL pipeline."""

    steps = [
        ("Extract customers", ETL_DIR / "extract" / "export_customers_csv.py"),
        ("Transform customers", ETL_DIR / "transform" / "transform_customers.py"),
        ("Load customers", ETL_DIR / "load" / "load_customers.py"),
        ("Validate customer data", ETL_DIR / "data_quality.py"),
        ("Extract products", ETL_DIR / "extract" / "export_products_csv.py"),
        ("Transform products", ETL_DIR / "transform" / "transform_products.py"),
        ("Load products", ETL_DIR / "load" / "load_products.py"),
        ("Extract orders", ETL_DIR / "extract" / "export_orders_csv.py"),
        ("Transform orders", ETL_DIR / "transform" / "transform_orders.py"),
        ("Load orders", ETL_DIR / "load" / "load_orders.py"),
    ]

    try:
        for step_name, script_path in steps:
            run_step(step_name, script_path)

        print("\nCustomer ETL pipeline completed successfully!")

    except subprocess.CalledProcessError as error:
        print(f"\nPipeline failed while running a step. Exit code: {error.returncode}")
        sys.exit(error.returncode)


if __name__ == "__main__":
    main()