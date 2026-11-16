# File events mode
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.useManagedFileEvents", "true")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/iot/_schema")
    .load("s3://acme-landing/iot/"))       # path under a UC external location
