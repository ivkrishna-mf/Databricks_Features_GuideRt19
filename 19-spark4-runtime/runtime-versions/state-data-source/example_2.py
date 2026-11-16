# Read state contents and find the biggest keys
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
state = (spark.read.format("statestore")
    .option("operatorId", 0)
    .load("/Volumes/main/ops/chk/device_5m"))
state.select("key.*", "value.*", "partition_id").show(5, truncate=False)
state.groupBy("partition_id").count().orderBy(F.desc("count")).show(5)
