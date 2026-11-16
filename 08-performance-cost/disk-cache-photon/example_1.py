# Check and enable the disk cache
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
print(spark.conf.get("spark.databricks.io.cache.enabled"))
spark.conf.set("spark.databricks.io.cache.enabled", "true")
spark.sql("CACHE SELECT order_id, amount FROM main.gold.fact_orders WHERE order_date >= '2026-01-01'")   # preload
