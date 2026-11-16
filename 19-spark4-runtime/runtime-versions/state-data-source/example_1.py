# List stateful operators in a checkpoint
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
meta = spark.read.format("state-metadata").load("/Volumes/main/ops/chk/device_5m")
meta.select("operatorId", "operatorName", "stateStoreName", "numPartitions",
            "minBatchId", "maxBatchId").show(truncate=False)
