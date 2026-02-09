import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
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

DATA_PATH = "D:/agno/agno/ml/churn_predict/data/vpn_churn.csv"
MODEL_PATH = "D:/agno/agno/ml/churn_predict/model/churn_model.pkl"

os.makedirs("model", exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)

    df["churn"] = df["churn"].map({"yes": 1, "no": 0})
    df.drop(columns=["customer_id"], inplace=True)

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

    print(" Model trained & saved")

if __name__ == "__main__":
    main()
