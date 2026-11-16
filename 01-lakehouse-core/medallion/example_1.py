# Bronze: raw plus metadata
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
bronze = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders_schema")
    .load("/Volumes/main/landing/orders/")
    .select("*", F.col("_metadata.file_path").alias("src_file"),
            F.current_timestamp().alias("ingested_at")))
