# Streaming table from an append-only source
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp

@dp.table(name="silver_events", table_properties={"pipelines.reset.allowed": "false"})
def silver_events():
    return (spark.readStream.table("bronze_events")
        .where("event_type IS NOT NULL"))
