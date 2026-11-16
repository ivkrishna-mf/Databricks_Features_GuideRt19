# Kinesis in a pipeline, parsed to VARIANT
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_clicks")
def bronze_clicks():
    return (spark.readStream.format("kinesis")
        .option("streamName", "clicks")
        .option("initialPosition", "TRIM_HORIZON")
        .load()
        .select(F.parse_json(F.col("data").cast("string")).alias("payload"),
                "approximateArrivalTimestamp"))
