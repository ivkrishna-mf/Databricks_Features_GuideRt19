# Transformations as functions, chained with transform
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import DataFrame, functions as F

def with_net(df: DataFrame, rate: float) -> DataFrame:
    return df.withColumn("net", F.round(F.col("gross") / (1 + rate), 2))

def only_paid(df: DataFrame) -> DataFrame:
    return df.where("status = 'PAID'")

silver = spark.table("main.bronze.orders").transform(only_paid).transform(with_net, 0.2)
