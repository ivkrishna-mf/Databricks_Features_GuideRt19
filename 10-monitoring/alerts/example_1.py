# Freshness check query behind an alert
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
fresh = spark.sql("""
SELECT timestampdiff(MINUTE, max(ingested_at), current_timestamp()) AS minutes_stale
FROM main.silver.orders""")
# Alert condition in the UI or API: minutes_stale > 90
