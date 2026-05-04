"""
load.py — Saves the cleaned DataFrame into a SQLite database.
"""

import pandas as pd
from sqlalchemy import create_engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.extract import extract
from src.etl.transform import transform

# SQLite database file will be created in the project root
DB_PATH = "shipment_warehouse.db"


def load(df):
    print("[1] Connecting to database...")
    engine = create_engine(f"sqlite:///{DB_PATH}")

    print("[2] Saving cleaned data to database...")
    df.to_sql("shipments", engine, if_exists="replace", index=False)

    print(f"[3] Done! {len(df):,} rows saved to table 'shipments'")
    print(f"    Database file: {DB_PATH}")


if __name__ == "__main__":
    raw_df   = extract()
    clean_df = transform(raw_df)
    load(clean_df)