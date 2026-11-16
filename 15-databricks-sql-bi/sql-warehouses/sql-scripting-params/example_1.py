# Safe parameters from Python
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
tbl = "main.gold.fact_orders"
df = spark.sql(
    "SELECT region, SUM(amount) AS revenue FROM IDENTIFIER(:tbl) WHERE order_date >= :d GROUP BY region",
    args={"tbl": tbl, "d": "2026-11-01"})
