import pandas as pd
import joblib
from fastapi import APIRouter
from pydantic import BaseModel
from database import engine
from churn_analyser import predict_with_shap
from churn_explainer import generate_explanation
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model/churn_model.pkl")

model = joblib.load(MODEL_PATH)

class Request(BaseModel):
    gmail_ids: list[str]

@router.post("/predict")
def predict(req: Request):

    query = """
        SELECT * FROM vpn_churn_test
        WHERE gmail_id = ANY(%s)
    """

    df = pd.read_sql(query, engine, params=(req.gmail_ids,))

    if df.empty:
        return {"results": [], "message": "No matching gmail_id found."}

    records = df.to_dict(orient="records")
    preds = predict_with_shap(model, records)

    output = []
    for p in preds:
        exp = generate_explanation(p)
        output.append({
                        "gmail_id": p["gmail_id"],
                        "prediction": p["prediction"],
                        "probability": p["probability"],
                        **exp
                    })

    return {"results": output}


# If you need the SHAP values we can modify below 
# output.append({**p, **exp})