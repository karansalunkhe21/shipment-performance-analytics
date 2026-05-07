import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Step 1 — Load data from database
print("[1] Loading data...")
conn = sqlite3.connect("shipment_warehouse.db")
df = pd.read_sql("SELECT * FROM shipments", conn)
print(f"    Loaded {len(df):,} rows")

# Step 2 — Select features
print("[2] Preparing features...")
features = [
    'days_for_shipping_real',
    'days_for_shipment_scheduled',
    'order_item_quantity',
    'order_item_discount_rate',
    'order_item_product_price',
]

target = 'is_late'

# Drop rows with missing values in selected columns
df = df[features + [target]].dropna()
print(f"    Clean rows: {len(df):,}")



# Step 3 — Split data into train and test
print("[3] Splitting data...")
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"    Training rows : {len(X_train):,}")
print(f"    Testing rows  : {len(X_test):,}")

# Step 4 — Train the model
print("[4] Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("    Model trained successfully")

# Step 5 — Evaluate the model
print("[5] Evaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"    Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Step 6 — Feature Importance
print("\n[6] Feature Importance:")
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance.to_string(index=False))