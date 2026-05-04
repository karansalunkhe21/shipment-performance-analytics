"""
transform.py — Cleans and prepares the raw DataFrame for analysis.
"""

import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.extract import extract


def clean_column_names(df):
    """Convert messy column names to clean snake_case."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df


def drop_useless_columns(df):
    """Remove PII and columns with no analytical value."""
    cols_to_drop = [
        "customer_email",
        "customer_password",
        "customer_fname",
        "customer_lname",
        "product_image",
        "product_description",
    ]
    df = df.drop(columns=cols_to_drop, errors="ignore")
    return df


def fix_dates(df):
    """Convert date columns from strings to proper datetime objects."""
    df["order_date_dateorders"] = pd.to_datetime(
        df["order_date_dateorders"], errors="coerce"
    )
    df["shipping_date_dateorders"] = pd.to_datetime(
        df["shipping_date_dateorders"], errors="coerce"
    )
    return df


def add_new_columns(df):
    """Create new columns useful for KPI analysis."""
    # 1 = late, 0 = on time
    df["is_late"] = (df["late_delivery_risk"] == 1).astype(int)

    # How many days delayed vs scheduled
    df["shipping_delay_days"] = (
        df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]
    )
    return df


def transform(df):
    print("[1] Cleaning column names...")
    df = clean_column_names(df)

    print("[2] Dropping useless columns...")
    df = drop_useless_columns(df)

    print("[3] Fixing date columns...")
    df = fix_dates(df)

    print("[4] Adding new columns...")
    df = add_new_columns(df)

    print(f"[5] Done! Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    raw_df = extract()
    clean_df = transform(raw_df)

    print("\nCleaned column names:")
    print(clean_df.columns.tolist())

    print("\nSample of new columns:")
    print(clean_df[["is_late", "shipping_delay_days"]].head())