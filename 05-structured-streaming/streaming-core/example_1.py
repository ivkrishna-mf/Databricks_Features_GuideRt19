# Scheduled incremental batch
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
(spark.readStream.table("main.bronze.orders")
    .where("status IS NOT NULL")
    .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/silver_orders")
    .trigger(availableNow=True)
    .toTable("main.silver.orders"))
