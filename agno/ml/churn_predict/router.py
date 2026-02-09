import pandas as pd
import joblib
from fastapi import APIRouter
from pydantic import BaseModel
from churn_analyser import predict_with_shap
from churn_explainer import generate_explanation

router = APIRouter()
model = joblib.load("D:/agno/agno/ml/churn_predict/model/churn_model.pkl")
df = pd.read_csv("D:/agno/agno/ml/churn_predict/data/vpn_churn_test.csv")

class Request(BaseModel):
    customer_ids: list[int]

@router.post("/predict")
def predict(req: Request):
    rows = df[df["customer_id"].isin(req.customer_ids)]
    records = rows.to_dict(orient="records")

    preds = predict_with_shap(model, records)

    output = []
    for p in preds:
        exp = generate_explanation(p)
        output.append({**p, **exp})

    return {"results": output}
