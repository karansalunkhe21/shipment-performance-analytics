import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("shipment_warehouse.db")

# KPI 1: On-Time Delivery Rate
query = """
SELECT
    COUNT(*)                                                         AS total_orders,
    SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END)                   AS on_time_orders,
    SUM(is_late)                                                     AS late_orders,
    ROUND(100.0 * SUM(CASE WHEN is_late = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
                                                                     AS otd_pct
FROM shipments;
"""

result = pd.read_sql(query, conn)
print(result)