# History, time travel and restore
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df.write.mode("append").saveAsTable("main.sales.orders")

(spark.sql("DESCRIBE HISTORY main.sales.orders")
    .select("version", "timestamp", "operation", "operationMetrics")
    .show(5, truncate=False))

before = spark.read.option("versionAsOf", 12).table("main.sales.orders")
spark.sql("RESTORE TABLE main.sales.orders TO VERSION AS OF 12")
