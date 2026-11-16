# Parse, store and extract
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
raw = spark.table("main.bronze.events_raw")                 # column: body STRING
v = raw.select(F.parse_json("body").alias("payload"))
out = v.select(
    F.variant_get("payload", "$.user.id", "string").alias("user_id"),
    F.try_variant_get("payload", "$.cart.total", "decimal(18,2)").alias("total"))
