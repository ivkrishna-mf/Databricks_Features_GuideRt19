# Historical snapshots: process dated folders in order
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp

def next_snapshot(latest_version):
    days = sorted(int(f.name.strip("/")) for f in dbutils.fs.ls("/Volumes/main/landing/products/"))
    todo = [d for d in days if latest_version is None or d > latest_version]
    if not todo:
        return None                       # nothing new: stop
    d = todo[0]
    return (spark.read.parquet("/Volumes/main/landing/products/" + str(d)), d)

dp.create_streaming_table("dim_product_hist")
dp.create_auto_cdc_from_snapshot_flow(
    target="dim_product_hist", source=next_snapshot,
    keys=["sku"], stored_as_scd_type=2)
