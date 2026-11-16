# Same files, three ways: one-off, incremental, scheduled
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
path = "/Volumes/main/landing/orders/"
once = spark.read.format("json").load(path)                         # one-off load, no state

incremental = (spark.readStream.format("cloudFiles")                  # Auto Loader, exactly once
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders/_schema")
    .load(path))

spark.sql(f"COPY INTO main.bronze.orders FROM '{path}' FILEFORMAT = JSON "
          "COPY_OPTIONS ('mergeSchema' = 'true')")                   # idempotent SQL load
