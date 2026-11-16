# Log a feature-aware model and score by key
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import mlflow
fe.log_model(model=model, artifact_path="model", flavor=mlflow.sklearn,
             training_set=training_set, registered_model_name="main.ml.churn_fs_model")

scored = fe.score_batch(model_uri="models:/main.ml.churn_fs_model@champion",
                        df=spark.table("main.ml.customers_to_score"))   # only keys needed
