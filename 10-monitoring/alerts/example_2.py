# Fail the task when data is stale, so job alerts fire
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
stale = (spark.table("main.silver.orders")
    .agg(F.expr("timestampdiff(MINUTE, max(ingested_at), current_timestamp())").alias("m"))
    .first()["m"])
if stale is None or stale > 90:
    raise RuntimeError(f"main.silver.orders is {stale} minutes stale")   # on_failure notification
