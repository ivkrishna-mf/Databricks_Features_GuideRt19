# pandas syntax, distributed
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import pyspark.pandas as ps
psdf = ps.read_table("main.silver.orders")
summary = (psdf[psdf["amount"] > 0]
    .groupby("country")["amount"].agg(["sum", "mean", "count"])
    .sort_values("sum", ascending=False))
summary.head(10)
sdf = psdf.to_spark()      # back to a Spark DataFrame
