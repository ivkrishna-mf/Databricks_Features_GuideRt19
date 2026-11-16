# Managed Iceberg table and a UniForm Delta table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.gold.orders_ice (order_id BIGINT, amount DECIMAL(18,2), order_date DATE)
USING ICEBERG CLUSTER BY (order_date)""")

spark.sql("""
ALTER TABLE main.gold.fact_orders SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg')""")
