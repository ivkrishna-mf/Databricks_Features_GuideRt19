# Fact table clustered for its access pattern
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.gold.fact_orders (
  order_id BIGINT, customer_sk BIGINT, store_sk BIGINT,
  order_date DATE, amount DECIMAL(18,2))
CLUSTER BY (order_date, customer_sk)
TBLPROPERTIES ('delta.targetFileSize' = '256mb')""")
