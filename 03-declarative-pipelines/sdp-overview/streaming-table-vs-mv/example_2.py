# Materialized view over data that gets corrected
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_customer_ltv")
def gold_customer_ltv():
    orders = spark.read.table("silver_orders")
    customers = spark.read.table("silver_customers")     # SCD1, rows change
    return (orders.join(customers, "customer_id")
        .groupBy("customer_id", "segment")
        .agg(F.sum("amount").alias("lifetime_value")))
