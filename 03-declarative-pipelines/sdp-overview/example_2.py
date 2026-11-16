# Gold materialized view
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_daily_revenue")
def gold_daily_revenue():
    return (spark.read.table("silver_orders")
        .groupBy(F.to_date("order_ts").alias("order_date"))
        .agg(F.sum("amount").alias("revenue"), F.count("*").alias("orders")))
