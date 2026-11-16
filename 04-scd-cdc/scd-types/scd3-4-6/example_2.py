# Type 4: current table and a history table from one feed
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql.functions import col
for name, scd in [("customer_current", 1), ("customer_history", 2)]:
    dp.create_streaming_table(name)
    dp.create_auto_cdc_flow(target=name, source="customers_cdc", keys=["customer_id"],
        sequence_by=col("commit_ts"), stored_as_scd_type=scd, name=name + "_flow")
