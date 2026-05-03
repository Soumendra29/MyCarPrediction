import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "car_data.csv")

data = pd.read_csv(file_path)
data.columns = data.columns.str.strip()

# Keep only useful columns
useful_cols = ['name', 'year', 'selling_price', 'km_driven', 'fuel', 
               'seller_type', 'transmission', 'owner', 
               'mileage', 'engine', 'max_power', 'seats']
data = data[useful_cols]

# Clean string columns — remove units
data['mileage'] = data['mileage'].astype(str).str.extract(r'([\d.]+)').astype(float)
data['engine'] = data['engine'].astype(str).str.extract(r'([\d.]+)').astype(float)
data['max_power'] = data['max_power'].astype(str).str.extract(r'([\d.]+)').astype(float)

# Remove corrupt or invalid name rows
data = data[data['name'].str.len() > 5]
print("After name filter:", len(data))

# Remove duplicate rows
data = data.drop_duplicates()
print("After duplicates removed:", len(data))

# Remove invalid year rows
data = data[data['year'] >= 2000]
data = data[data['year'] <= 2024]

# Remove invalid km rows
data = data[data['km_driven'] > 0]
data = data[data['km_driven'] <= 500000]

# Remove price outliers
Q1 = data['selling_price'].quantile(0.05)
Q3 = data['selling_price'].quantile(0.95)
data = data[data['selling_price'] >= Q1]
data = data[data['selling_price'] <= Q3]
print("Price range:", data['selling_price'].min(), "to", data['selling_price'].max())

# Drop name column
data = data.drop(["name"], axis=1)

# Owner mapping
data["owner"] = data["owner"].map({
    "First Owner": 1,
    "Second Owner": 2,
    "Third Owner": 3,
    "Fourth & Above Owner": 4,
    "Test Drive Car": 0
})

# Drop NaN rows
data = data.dropna()
print("Final clean rows:", len(data))

# Create dummy columns
data = pd.get_dummies(data, columns=["fuel", "seller_type", "transmission"], drop_first=False)

X = data.drop("selling_price", axis=1)
y = data["selling_price"]

# Log transform for better accuracy
y = np.log1p(y)

# Scale numeric columns
scaler = StandardScaler()
scale_cols = ["km_driven", "year", "mileage", "engine", "max_power", "seats"]
scale_cols = [col for col in scale_cols if col in X.columns]
X[scale_cols] = scaler.fit_transform(X[scale_cols])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.03,
    max_depth=6,
    min_samples_split=5,
    min_samples_leaf=3,
    subsample=0.8,
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print(f"\nModel Accuracy: {score:.4f}")

# Save model and related files
pickle.dump(model, open(os.path.join(current_dir, "model.pkl"), "wb"))
pickle.dump(X.columns.tolist(), open(os.path.join(current_dir, "columns.pkl"), "wb"))
pickle.dump(scaler, open(os.path.join(current_dir, "scaler.pkl"), "wb"))
pickle.dump(scale_cols, open(os.path.join(current_dir, "scale_cols.pkl"), "wb"))

print("Model saved successfully!")