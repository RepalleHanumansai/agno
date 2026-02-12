import pandas as pd
import shap

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

def predict_with_shap(model, records):
    results = []
    explainer = shap.TreeExplainer(model.named_steps["clf"])

    for r in records:
        gid = r.get("gmail_id", "unknown")
        df = pd.DataFrame([r]).drop(columns=["gmail_id"], errors="ignore")

        df[CATEGORICAL] = df[CATEGORICAL].fillna("").astype(str)
        df[NUMERICAL] = df[NUMERICAL].apply(
            pd.to_numeric, errors="coerce"
        ).fillna(0.0)

        pred = int(model.predict(df)[0])
        prob = float(model.predict_proba(df)[0][1] * 100)

        Xt = model.named_steps["prep"].transform(df)
        shap_vals = explainer.shap_values(Xt)[1][0]

        shap_dict = dict(zip(CATEGORICAL + NUMERICAL, shap_vals))

        results.append({
            "gmail_id": gid,
            "prediction": pred,
            "probability": round(prob, 2),
            "shap": shap_dict
        })

    return results
