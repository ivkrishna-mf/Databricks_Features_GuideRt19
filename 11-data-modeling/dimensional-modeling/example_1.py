# Materialized view for a pre-computed aggregate
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_sales_by_store_day", cluster_by=["order_date"])
def gold_sales_by_store_day():
    f = spark.read.table("main.gold.fact_orders")
    s = spark.read.table("main.gold.dim_store")
    return (f.join(s, "store_sk").groupBy("order_date", "store_sk", "region")
        .agg(F.sum("amount").alias("revenue"), F.countDistinct("order_id").alias("orders")))
