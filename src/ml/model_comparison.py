import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# Step 1 — Load data
print("[1] Loading data...")
conn = sqlite3.connect("shipment_warehouse.db")
df = pd.read_sql("SELECT * FROM shipments", conn)
print(f"    Loaded {len(df):,} rows")

# Step 2 — Add more features this time
print("[2] Preparing features...")

# Encode categorical columns
df['shipping_mode_encoded'] = df['shipping_mode'].astype('category').cat.codes
df['market_encoded'] = df['market'].astype('category').cat.codes
df['order_status_encoded'] = df['order_status'].astype('category').cat.codes
df['customer_segment_encoded'] = df['customer_segment'].astype('category').cat.codes

# Step 2 revised — only use features known BEFORE shipment
features = [
    'days_for_shipment_scheduled',  # promised delivery time
    'order_item_quantity',
    'order_item_discount_rate',
    'order_item_product_price',
    'shipping_mode_encoded',
    'market_encoded',
    'customer_segment_encoded',
]

target = 'is_late'

df = df[features + [target]].dropna()
print(f"    Features: {len(features)}")
print(f"    Clean rows: {len(df):,}")



# Step 3 — Split data
print("\n[3] Splitting data...")
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"    Training rows : {len(X_train):,}")
print(f"    Testing rows  : {len(X_test):,}")

# Step 4 — Train and compare 3 models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost":             XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
}

results = {}

for name, model in models.items():
    print(f"\n[Training] {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy
    print(f"    Accuracy: {accuracy * 100:.2f}%")

# Step 5 — Summary
print("\n" + "="*40)
print("MODEL COMPARISON SUMMARY")
print("="*40)
for name, acc in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"  {name:<25} : {acc * 100:.2f}%")



 # Step 6 — XGBoost Feature Importance
import matplotlib.pyplot as plt

xgb_model = models["XGBoost"]
importance = pd.DataFrame({
    'feature': features,
    'importance': xgb_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nXGBoost Feature Importance:")
print(importance.to_string(index=False))

importance.plot(
    kind='barh',
    x='feature',
    y='importance',
    color='steelblue',
    edgecolor='black',
    legend=False
)
plt.title('XGBoost Feature Importance')
plt.xlabel('Importance')
plt.tight_layout()
plt.show()