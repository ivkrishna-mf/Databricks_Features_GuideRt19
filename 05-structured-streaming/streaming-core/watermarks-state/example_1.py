# Tumbling window aggregation with late data bound
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
agg = (spark.readStream.table("main.silver.events")
    .withWatermark("event_ts", "10 minutes")
    .groupBy(F.window("event_ts", "5 minutes"), "device_id")
    .agg(F.count("*").alias("events"), F.avg("temp").alias("avg_temp")))
(agg.writeStream.outputMode("append")
    .option("checkpointLocation", "/Volumes/main/ops/chk/device_5m")
    .toTable("main.gold.device_5m"))
