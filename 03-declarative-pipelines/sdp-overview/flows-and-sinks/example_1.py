# Two flows into one streaming table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
dp.create_streaming_table("bronze_orders_all")

@dp.append_flow(target="bronze_orders_all", name="orders_eu")
def orders_eu():
    return spark.readStream.table("main.bronze.orders_eu")

@dp.append_flow(target="bronze_orders_all", name="orders_us")
def orders_us():
    return spark.readStream.table("main.bronze.orders_us")
