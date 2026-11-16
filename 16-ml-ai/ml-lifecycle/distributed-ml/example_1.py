# Spark ML pipeline
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import GBTClassifier
import mlflow
mlflow.pyspark.ml.autolog()

df = spark.table("main.ml.churn_training")
pipe = Pipeline(stages=[
    StringIndexer(inputCol="plan", outputCol="plan_idx", handleInvalid="keep"),
    VectorAssembler(inputCols=["plan_idx", "tenure", "monthly_spend"], outputCol="features"),
    GBTClassifier(labelCol="churned", featuresCol="features", maxIter=50)])
train, test = df.randomSplit([0.8, 0.2], seed=7)
model = pipe.fit(train)
model.transform(test).select("churned", "prediction").show(5)
