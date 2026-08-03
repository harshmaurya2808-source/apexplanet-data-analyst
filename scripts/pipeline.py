"""
pipeline.py
Automated data pipeline for the ApexPlanet Data Analytics Internship (Task 5).

What it does:
    1. Loads the raw Superstore dataset
    2. Cleans it (missing values, duplicates, data types, outliers)
    3. Saves the cleaned dataset back to /data
    4. Calculates key business KPIs
    5. Exports both the cleaned data and the KPI summary to an Excel file

Usage:
    python scripts/pipeline.py

Can be scheduled via:
    - GitHub Actions (see .github/workflows/pipeline.yml)
    - Windows Task Scheduler (point it at this script + your venv's python.exe)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIG — adjust these paths if your folder structure differs
# ---------------------------------------------------------------------------
RAW_DATA_PATH = Path("data/superstore_sales.csv")
CLEANED_DATA_PATH = Path("data/cleaned_superstore_sales_auto.csv")
EXCEL_OUTPUT_PATH = Path("reports/superstore_kpi_report.xlsx")


def load_data(path: Path) -> pd.DataFrame:
    """Load the raw dataset."""
    print(f"[1/5] Loading raw data from {path} ...")
    df = pd.read_csv(path, encoding="latin1")
    print(f"      Loaded {len(df):,} rows.")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset: standardize columns, handle missing values,
    duplicates, data types, and flag outliers."""
    print("[2/5] Cleaning data ...")

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]

    # Drop rows missing critical Sales values
    before = len(df)
    df = df.dropna(subset=["sales"])

    # Fill missing text columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("Unknown")

    # Remove duplicates
    df = df.drop_duplicates()

    # Fix date types
    for date_col in ["order_date", "ship_date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Drop rows with unparseable dates (keeps downstream KPIs reliable)
    df = df.dropna(subset=[c for c in ["order_date", "ship_date"] if c in df.columns])

    # Flag outliers in Sales using IQR method (flagged, not removed)
    Q1 = df["sales"].quantile(0.25)
    Q3 = df["sales"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df["sales_outlier"] = (df["sales"] < lower_bound) | (df["sales"] > upper_bound)

    removed = before - len(df)
    print(f"      Removed {removed:,} rows during cleaning. {len(df):,} rows remain.")
    return df


def save_cleaned_data(df: pd.DataFrame, path: Path) -> None:
    """Save the cleaned dataset to CSV."""
    print(f"[3/5] Saving cleaned data to {path} ...")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate key business KPIs and return them as a summary DataFrame."""
    print("[4/5] Calculating KPIs ...")

    kpis = {
        "Total Sales": df["sales"].sum(),
        "Total Orders": df["order_id"].nunique() if "order_id" in df.columns else len(df),
        "Total Customers": df["customer_name"].nunique() if "customer_name" in df.columns else np.nan,
        "Average Order Value": df["sales"].mean(),
        "Total Quantity Sold": df["quantity"].sum() if "quantity" in df.columns else np.nan,
        "Total Profit": df["profit"].sum() if "profit" in df.columns else np.nan,
        "Average Discount": df["discount"].mean() if "discount" in df.columns else np.nan,
        "Outlier Order Count": int(df["sales_outlier"].sum()),
        "Report Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
    print("      KPIs calculated:")
    for k, v in kpis.items():
        print(f"        {k}: {v}")
    return kpi_df


def export_to_excel(df: pd.DataFrame, kpi_df: pd.DataFrame, path: Path) -> None:
    """Export both the cleaned dataset and the KPI summary into one Excel file,
    each on its own sheet."""
    print(f"[5/5] Exporting to Excel at {path} ...")
    path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        kpi_df.to_excel(writer, sheet_name="KPI Summary", index=False)
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)

    print("      Done.")


def main():
    print("=" * 60)
    print("ApexPlanet Data Analytics Internship — Automated Pipeline")
    print("=" * 60)

    df_raw = load_data(RAW_DATA_PATH)
    df_clean = clean_data(df_raw)
    save_cleaned_data(df_clean, CLEANED_DATA_PATH)
    kpi_df = calculate_kpis(df_clean)
    export_to_excel(df_clean, kpi_df, EXCEL_OUTPUT_PATH)

    print("=" * 60)
    print("Pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
