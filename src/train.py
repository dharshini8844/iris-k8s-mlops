"""Train a RandomForest on Iris, log everything to MLflow, save model + metrics."""
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
params = yaml.safe_load(open("params.yaml"))["train"]

train_df = pd.read_csv("data/train.csv")
test_df = pd.read_csv("data/test.csv")

# SQLite backend so the MLflow Model Registry works locally and in CI
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("iris-classifier")

with mlflow.start_run() as run:
    model = RandomForestClassifier(**params)
    model.fit(train_df[FEATURES], train_df["target"])

    preds = model.predict(test_df[FEATURES])
    metrics = {
        "accuracy": round(accuracy_score(test_df["target"], preds), 4),
        "f1_macro": round(f1_score(test_df["target"], preds, average="macro"), 4),
    }

    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="IrisModel",
        serialization_format="cloudpickle",
        input_example=test_df[FEATURES].head(2),
    )

    # Plain copy of the model for the API container
    Path("model").mkdir(exist_ok=True)
    joblib.dump(model, "model/model.pkl")
    json.dump(metrics, open("metrics.json", "w"), indent=2)

    print(f"Run ID: {run.info.run_id}")
    print(f"Metrics: {metrics}")
