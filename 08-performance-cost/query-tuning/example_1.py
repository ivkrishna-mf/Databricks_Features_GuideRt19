# Read the plan and fix a skewed join
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
orders = spark.table("main.silver.orders").where("customer_id IS NOT NULL")   # null keys skew
dims = spark.table("main.silver.customers")
joined = orders.join(dims.hint("broadcast"), "customer_id")
joined.explain("formatted")       # look for BroadcastHashJoin and PushedFilters
