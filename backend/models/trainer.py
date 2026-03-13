import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, precision_score, recall_score,precision_recall_curve,auc
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import os
from datetime import datetime
import re

class TextCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, column_name):
        self.column_name = column_name
    def fit(self, X, y=None): return self
    def transform(self, X):
        X_copy = pd.DataFrame(X).copy()
        X_copy[self.column_name] = X_copy[self.column_name].astype(str).apply(
            lambda text: re.sub(r'[^\w\s]', '', text).lower()
        )
        return X_copy[self.column_name]

def build_pipeline(X, model_instance):
    text_feature = ["sprint_description"]
    numerical_features = X.select_dtypes(exclude="object").columns.tolist()
    categorical_features = [col for col in X.select_dtypes(include="object").columns if col not in text_feature]

    numerical_pipeline = Pipeline(steps=[
        ("Imputer", SimpleImputer(strategy="median")),
        ("Scale", StandardScaler())
    ])

    vectorization_pipeline = Pipeline(steps=[
        ("Transform", TextCleaner(column_name="sprint_description")),
        ("Vectorizer", TfidfVectorizer(max_features=500, stop_words="english"))
    ])

    categorical_pipeline = Pipeline(steps=[
        ("Imputer", SimpleImputer(strategy="most_frequent")),
        ("OHE", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessing = ColumnTransformer(transformers=[
        ("Numerical", numerical_pipeline, numerical_features),
        ("Text", vectorization_pipeline, text_feature),
        ("Categorical", categorical_pipeline, categorical_features)
    ])

    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessing),
        ("Classifier", model_instance)
    ])

    return pipeline

def train_model(data):
  if not isinstance(data, pd.DataFrame):
    data = pd.DataFrame(data)

  X = data.drop(columns=["target_failed"])
  y = data["target_failed"]

  X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42,stratify=y,test_size=0.2)

  pipeline = build_pipeline(X_train,LogisticRegression())

  print("\nTraining...")
  pipeline.fit(X_train,y_train)
  y_pred = pipeline.predict(X_test)
  y_prob = pipeline.predict_proba(X_test)[:,1]

  precision_vals, recall_vals, thresholds = precision_recall_curve(y_test,y_prob)
  pr_auc_score = auc(recall_vals,precision_vals)
  with open(f"models/trained_model/trained_model_v1_{datetime.now().strftime('%Y-%m-%d')}.pkl","wb") as file:
      joblib.dump(pipeline,file)
  print("Model Training is Done")

  return {
      "f1_score":round(f1_score(y_test,y_pred,zero_division=0),4),
      "recall_score":round(recall_score(y_test,y_pred,zero_division=0),4),
      "precision_score":round(precision_score(y_test,y_pred,zero_division=0),4),
      "pr_auc_score":round(pr_auc_score,4)
  }

if __name__ == "__main__":
    #for testing the model efficiency 
    data = pd.read_csv("sprint_record.csv")
    model_ = train_model(data)
    new_sprint = {
        "team_seniority_ratio": 0.33,
        "code_churn_lines": 4500,
        "project_type": "Backend",
        "sprint_description": "Migrate legacy user auth to AWS Cognito. High risk of breaking changes.",
    }
    model = joblib.load(f"models/trained_model/trained_model_v1_{datetime.now().strftime('%Y-%m-%d')}.pkl")
    print(model.predict_proba(pd.DataFrame([new_sprint]))[:,1])