# Batch scoring with the champion model
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import mlflow
from pyspark.sql import functions as F
mlflow.set_registry_uri("databricks-uc")
predict = mlflow.pyfunc.spark_udf(spark, "models:/main.ml.churn_model@champion", result_type="double")

scored = (spark.table("main.ml.churn_features_today")
    .withColumn("churn_score", predict(*[c for c in feature_cols])))
scored.write.mode("overwrite").saveAsTable("main.ml.churn_scores")
