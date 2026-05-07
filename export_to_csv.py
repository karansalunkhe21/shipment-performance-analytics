import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("shipment_warehouse.db")

# Export shipments table to CSV
df = pd.read_sql("SELECT * FROM shipments", conn)
df.to_csv("data/processed/shipments_clean.csv", index=False)

print(f"Exported {len(df):,} rows to data/processed/shipments_clean.csv")