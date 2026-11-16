# The same source inside a Lakeflow pipeline
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_orders", comment="Raw orders from landing")
def bronze_orders():
    return (spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.schemaHints", "amount DECIMAL(18,2), order_ts TIMESTAMP")
        .load("/Volumes/main/landing/orders_csv/")
        .withColumn("src_file", F.col("_metadata.file_path")))
