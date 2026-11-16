# SCD type 1: keep the latest row
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.temporary_view
def customers_cdc():
    return spark.readStream.table("main.bronze.customers_cdc")

dp.create_streaming_table("silver_customers")
dp.create_auto_cdc_flow(
    target="silver_customers",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by=col("commit_ts"),
    apply_as_deletes=expr("op = 'DELETE'"),
    except_column_list=["op", "commit_ts"],
    stored_as_scd_type=1)
