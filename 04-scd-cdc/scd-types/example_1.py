# Point-in-time join of a fact to an SCD2 dimension
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
f = spark.table("main.gold.fact_orders").alias("f")
d = spark.table("main.gold.dim_customer_history").alias("d")
as_was = f.join(d,
    (F.col("f.customer_id") == F.col("d.customer_id")) &
    (F.col("f.order_ts") >= F.col("d.__START_AT")) &
    (F.col("d.__END_AT").isNull() | (F.col("f.order_ts") < F.col("d.__END_AT"))))
