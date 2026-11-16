# Classic notification mode with rate limits
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.useNotifications", "true")
    .option("cloudFiles.maxFilesPerTrigger", 500)
    .option("cloudFiles.maxBytesPerTrigger", "10g")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/clicks/_schema")
    .load("abfss://landing@acme.dfs.core.windows.net/clicks/"))
