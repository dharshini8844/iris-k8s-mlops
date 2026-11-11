"""FastAPI service for the Iris model with /predict and /health endpoints."""
import os

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "model/model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "dev")
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris Model API", version=MODEL_VERSION)

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:  # keep the app up so /health can report the problem
    model = None
    print(f"Model load failed: {e}")


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "model_version": MODEL_VERSION}


@app.post("/predict")
def predict(item: IrisInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    X = pd.DataFrame([item.model_dump()])
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0].max())
    return {
        "prediction": pred,
        "class_name": CLASS_NAMES[pred],
        "confidence": round(prob, 4),
        "model_version": MODEL_VERSION,
    }
