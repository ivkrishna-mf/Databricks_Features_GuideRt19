# Quarantine the rejected rows
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F
quarantine_cond = "NOT(" + " AND ".join("(" + r + ")" for r in rules.values()) + ")"

@dp.table(name="quarantine_orders")
def quarantine_orders():
    return (spark.readStream.table("bronze_orders")
        .where(F.expr(quarantine_cond) | F.expr("order_id IS NULL")))
