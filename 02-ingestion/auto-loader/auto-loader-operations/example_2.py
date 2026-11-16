# Skip history, pick up only new files
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.includeExistingFiles", "false")
    .option("cloudFiles.backfillInterval", "1 day")     # classic notification safety net
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/tx/_schema")
    .load("s3://acme-landing/tx/"))
