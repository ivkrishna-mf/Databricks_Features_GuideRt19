# Scheduled incremental run with file archiving
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/logs/_schema")
    .option("cloudFiles.cleanSource", "MOVE")
    .option("cloudFiles.cleanSource.moveDestination", "s3://acme-archive/logs/")
    .load("s3://acme-landing/logs/")
  .writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/logs")
    .trigger(availableNow=True).toTable("main.bronze.logs"))
