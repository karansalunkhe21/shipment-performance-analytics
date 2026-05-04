"""
extract.py — Reads the raw CSV file and loads it into a DataFrame.
"""

import pandas as pd

# Path to the dataset
CSV_PATH = "data/raw/DataCoSupplyChainDataset.csv"


def extract():
    print("[1] Loading dataset...")
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    print(f"[2] Done! Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    df = extract()
    print("\nFirst 5 rows:")
    print(df.head())