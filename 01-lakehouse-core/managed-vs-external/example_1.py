# Managed table with automatic clustering
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.silver.events (
  event_id STRING, user_id STRING, event_ts TIMESTAMP, payload VARIANT)
CLUSTER BY AUTO""")
