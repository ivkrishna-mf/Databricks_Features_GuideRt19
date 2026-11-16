# The same in Structured Streaming: you own the plumbing
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
q = (spark.readStream.table("main.bronze.payments")
    .withWatermark("paid_at", "2 hours")
    .dropDuplicatesWithinWatermark(["payment_id"])
    .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/silver_payments")
    .trigger(processingTime="1 minute")
    .toTable("main.silver.payments"))
