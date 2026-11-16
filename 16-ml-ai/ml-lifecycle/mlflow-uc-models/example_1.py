# Log with signature and register
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import mlflow
from mlflow.models import infer_signature
mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    sig = infer_signature(X_tr, model.predict(X_tr))
    mlflow.sklearn.log_model(model, name="model", signature=sig, input_example=X_tr.head(3),
                             registered_model_name="main.ml.churn_model")
