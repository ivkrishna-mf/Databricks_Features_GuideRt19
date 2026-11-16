# Periodic snapshot: read the latest table state each update
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp

@dp.temporary_view
def products_snapshot():
    return spark.read.table("main.staging.products_full")

dp.create_streaming_table("dim_product")
dp.create_auto_cdc_from_snapshot_flow(
    target="dim_product",
    source="products_snapshot",
    keys=["sku"],
    stored_as_scd_type=2)
