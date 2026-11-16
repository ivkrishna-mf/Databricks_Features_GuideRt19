# One table readable as Delta and Iceberg
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
ALTER TABLE main.gold.fact_orders SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg')""")
# A managed Iceberg table instead
spark.sql("CREATE TABLE main.gold.dim_store_ice (store_sk BIGINT, name STRING) USING ICEBERG")
