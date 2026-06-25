import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

print("Loading dataset...")

df = pd.read_csv(
    "data/master_dataset.csv"
)

print(
    "Original Shape:",
    df.shape
)

# Reduce size if huge

if len(df) > 50000:

    df = df.sample(
        n=50000,
        random_state=42
    )

print(
    "Training Shape:",
    df.shape
)

# Improved Features

features = [
    "RSI",
    "MACD",
    "ATR",
    "Volatility",
    "BB_Upper",
    "BB_Lower",
    "EMA20",
    "EMA50",
    "SMA20",
    "SMA50",
    "Momentum",
    "Trend"
]

# Remove rows with missing values

df = df.dropna(
    subset=features + ["Target"]
)

X = df[features]

y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "\nAccuracy:",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print(
    "\nFeature Importance:"
)

importance = pd.DataFrame({
    "Feature": features,
    "Importance":
    model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    "models/random_forest.pkl"
)

print(
    "\nModel Saved Successfully"
)