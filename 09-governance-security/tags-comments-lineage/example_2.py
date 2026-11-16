# Who reads this table? Lineage from system tables
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
SELECT DISTINCT target_table_full_name, entity_type, created_by
FROM system.access.table_lineage
WHERE source_table_full_name = 'main.silver.orders'
  AND event_time >= current_date() - INTERVAL 30 DAYS""").show(truncate=False)
