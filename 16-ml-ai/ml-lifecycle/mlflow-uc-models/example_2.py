# Promote with aliases and load by alias
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from mlflow import MlflowClient
client = MlflowClient(registry_uri="databricks-uc")
latest = max(int(v.version) for v in client.search_model_versions("name='main.ml.churn_model'"))
current = client.get_model_version_by_alias("main.ml.churn_model", "champion")
client.set_registered_model_alias("main.ml.churn_model", "previous", current.version)
client.set_registered_model_alias("main.ml.churn_model", "champion", latest)

model = mlflow.pyfunc.load_model("models:/main.ml.churn_model@champion")
