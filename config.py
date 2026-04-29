"""
config.py — Central settings for the Shipment Performance Analytics project.

Every other module imports from here.
To switch databases, change DB_URL only — nothing else needs to change.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # reads a .env file if present (useful for passwords)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR      = Path(__file__).parent          # root of the project
DATA_RAW_DIR  = BASE_DIR / "data" / "raw"
OUTPUTS_DIR   = BASE_DIR / "outputs"

RAW_CSV       = DATA_RAW_DIR / "DataCoSupplyChainDataset.csv"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# Default: SQLite (no server needed, file sits in your project folder)
# To use PostgreSQL, create a .env file and add:
#   DATABASE_URL=postgresql://user:password@localhost/shipment_db
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'shipment_warehouse.db'}")

# ---------------------------------------------------------------------------
# ETL settings
# ---------------------------------------------------------------------------
CSV_ENCODING   = "latin-1"   # DataCo uses latin-1 encoding
LOAD_IF_EXISTS = "replace"   # replace table on each run (safe default)

# Columns removed immediately after loading — PII, no analytical value
DROP_COLUMNS = [
    "customer_email",
    "customer_password",
    "customer_fname",
    "customer_lname",
    "product_image",
]
