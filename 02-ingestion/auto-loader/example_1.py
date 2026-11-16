# Incremental JSON ingestion as a scheduled batch
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders/_schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("/Volumes/main/landing/orders/")
  .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/orders")
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable("main.bronze.orders"))
