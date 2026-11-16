# Lazy plan, one action, read the plan
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
orders = spark.table("main.silver.orders")             # nothing runs yet
big = (orders.where("order_date >= '2026-10-01'")       # narrow
    .groupBy("customer_id")                              # wide: shuffle
    .agg(F.sum("amount").alias("spend")))
big.explain("formatted")       # Exchange = shuffle; PushedFilters = file skipping
big.write.mode("overwrite").saveAsTable("main.gold.spend_oct")   # the action
