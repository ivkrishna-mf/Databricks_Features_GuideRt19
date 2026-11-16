# Bronze streaming table and silver with a quality rule
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_orders")
def bronze_orders():
    return (spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/Volumes/main/landing/orders/"))

@dp.table(name="silver_orders")
@dp.expect_or_drop("valid_id", "order_id IS NOT NULL")
def silver_orders():
    return (spark.readStream.table("bronze_orders")
        .withColumn("order_ts", F.to_timestamp("order_ts")))
