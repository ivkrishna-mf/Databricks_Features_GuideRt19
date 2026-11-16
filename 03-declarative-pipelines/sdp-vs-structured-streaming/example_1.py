# Deduplicated silver table in SDP
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp

@dp.table(name="silver_payments")
def silver_payments():
    return (spark.readStream.table("bronze_payments")
        .withWatermark("paid_at", "2 hours")
        .dropDuplicatesWithinWatermark(["payment_id"]))
