# Broadcast join and a running total
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F, Window
sales = spark.table("main.silver.sales")
stores = spark.table("main.silver.stores")
joined = sales.join(F.broadcast(stores), "store_id")

w = (Window.partitionBy("store_id").orderBy("sale_date")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow))
daily = (joined.groupBy("store_id", "sale_date").agg(F.sum("amount").alias("revenue"))
    .withColumn("running_revenue", F.sum("revenue").over(w)))
