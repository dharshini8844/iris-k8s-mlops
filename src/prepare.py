"""Load the Iris dataset and split it into train and test CSV files."""
from pathlib import Path

import pandas as pd
import yaml
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

params = yaml.safe_load(open("params.yaml"))["prepare"]

iris = load_iris(as_frame=True)
df = iris.frame.rename(columns={
    "sepal length (cm)": "sepal_length",
    "sepal width (cm)": "sepal_width",
    "petal length (cm)": "petal_length",
    "petal width (cm)": "petal_width",
})

train_df, test_df = train_test_split(
    df,
    test_size=params["test_size"],
    random_state=params["random_state"],
    stratify=df["target"],
)

Path("data").mkdir(exist_ok=True)
train_df.to_csv("data/train.csv", index=False)
test_df.to_csv("data/test.csv", index=False)
print(f"Train rows: {len(train_df)}, Test rows: {len(test_df)}")
