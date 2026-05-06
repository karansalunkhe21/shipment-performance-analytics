# 🚚 Shipment Performance Analytics

An end-to-end supply chain analytics project built on the **DataCo Smart Supply Chain dataset** (180,000+ orders). This project covers the full data pipeline — from raw data ingestion to interactive dashboards — using Python, SQL, Google BigQuery, and Looker Studio.

---

## 📊 Live Dashboard

🔗 [View Interactive Dashboard](https://datastudio.google.com/reporting/5945d25a-c070-46ec-bd79-f805574bd4ab)

The dashboard includes:
- KPI scorecards — Total Orders, Revenue, Profit, Late Orders
- OTD% by Shipping Mode
- Revenue by Product Category
- Monthly Revenue Trend (2015–2018)
- Late Orders by Country (Geo Map)
- Filters by Date, Shipping Mode, and Market

---

## 🗂️ Project Structure

```
shipment-performance-analytics/
│
├── data/
│   ├── raw/                  ← raw CSV (git-ignored)
│   └── processed/            ← cleaned CSV exported for BigQuery
│
├── src/
│   ├── etl/
│   │   ├── extract.py        ← load raw CSV into DataFrame
│   │   ├── transform.py      ← clean, normalise, feature engineer
│   │   └── load.py           ← save cleaned data to SQLite
│   │
│   └── sql/
│       ├── kpi_queries.sql   ← core KPI queries
│       └── advanced/
│           └── advanced_queries.sql  ← window functions, CTEs
│
├── notebooks/                ← EDA and analysis (coming soon)
├── tests/                    ← unit tests (coming soon)
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | ETL pipeline — extract, clean, load |
| pandas | Data cleaning and transformation |
| SQLite | Local data warehouse |
| SQL | KPI analysis and advanced queries |
| Google BigQuery | Cloud data warehouse |
| Looker Studio | Interactive dashboard |
| DBeaver | SQL client |
| GitHub | Version control |

---

## 📦 Dataset

| Property | Value |
|----------|-------|
| Source | DataCo Global / Kaggle |
| Rows | 180,519 |
| Columns | 53 |
| Date Range | Jan 2015 – Jan 2018 |
| Industries | Clothing, Sports, Electronics |
| Markets | 164 countries, 6 global regions |

---

## 🔍 Key Findings

| KPI | Result | Insight |
|-----|--------|---------|
| Overall OTD% | 45.17% | More than half of all orders are late |
| First Class OTD% | 4.68% | Customers paying premium get worst service |
| Top Revenue Category | Fishing — $6.9M | Single category drives significant revenue |
| Discount Impact | Profit drops from $26 → $18 | Discounts hurt profit without increasing sales |
| Late Delivery Trend | Stuck at 53–57% for 3 years | No improvement over time — structural problem |
| Top Department | Fan Shop — $17M revenue | Dominates all other departments |

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/karansalunkhe21/shipment-performance-analytics.git
cd shipment-performance-analytics
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add the dataset
Download `DataCoSupplyChainDataset.csv` from [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) and place it in `data/raw/`

### 5. Run the ETL pipeline
```bash
# Step 1 - Extract
python3 src/etl/extract.py

# Step 2 - Transform
python3 src/etl/transform.py

# Step 3 - Load
python3 src/etl/load.py
```

### 6. Explore SQL queries
Open `src/sql/kpi_queries.sql` or `src/sql/advanced/advanced_queries.sql` in DBeaver connected to `shipment_warehouse.db`

---

## 📈 SQL Analysis Covered

**Core KPIs:**
- Overall On-Time Delivery Rate (OTD%)
- OTD% by Shipping Mode
- OTD% by Region
- Revenue and Profit by Category
- Discount Impact on Profit Margin
- Customer Segment Analysis
- Monthly Revenue Trend

**Advanced Queries:**
- Running Total Revenue (CTE + Window Function)
- Month over Month Revenue Growth (LAG)
- Top 3 Products per Category (RANK + PARTITION BY)
- Customer Delivery Deterioration Analysis
- Revenue Contribution % per Category
- 3 Month Moving Average Late Delivery Rate
- Customer Lifetime Value Ranking (NTILE)

---

## 🔮 Coming Next
- Phase 5 — Machine Learning (Late Delivery Prediction)

---

## 👤 Author
**Karan Salunkhe**
[GitHub](https://github.com/karansalunkhe21)

---

## 📄 License
MIT License