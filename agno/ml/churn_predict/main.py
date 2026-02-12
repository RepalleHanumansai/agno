from fastapi import FastAPI
from router import router

app = FastAPI(title="VPN Churn Prediction API")
app.include_router(router)
