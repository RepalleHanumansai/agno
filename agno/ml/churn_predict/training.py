import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
from database import engine
import os

CATEGORICAL = [
    "gender","marital_status","seniorcitizen","auto_renewal",
    "subscription_type","feedback_sentiment","streaming_access",
    "average_speed_mbps","last_login","discount_used"
]

NUMERICAL = [
    "tenure","devices_connected","tickets_raised","monthly_usage_hours",
    "server_switch_frequency","connection_success_rate",
    "plan_upgrade_attempts","unresolved_tickets"
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model/churn_model.pkl")

os.makedirs("model", exist_ok=True)

def main():
    print("Loading training data from PostgreSQL...")
    df = pd.read_sql("SELECT * FROM vpn_churn_train", engine)

    df["churn"] = df["churn"].map({"yes": 1, "no": 0})

    if "gmail_id" in df.columns:
        df.drop(columns=["gmail_id"], inplace=True)

    X = df.drop("churn", axis=1)
    y = df["churn"]

    X[CATEGORICAL] = X[CATEGORICAL].fillna("").astype(str)
    X[NUMERICAL] = X[NUMERICAL].fillna(0).astype(float)

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAL),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL)
    ])

    model = Pipeline([
        ("prep", preprocessor),
        ("clf", LGBMClassifier(
            objective="binary",
            class_weight="balanced",
            n_estimators=400,
            learning_rate=0.05,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)

    print("Model trained & saved successfully!")

if __name__ == "__main__":
    main()
