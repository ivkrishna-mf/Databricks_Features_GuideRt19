# Find the most expensive queries from system tables
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
top = spark.sql("""
SELECT statement_id, executed_by, total_duration_ms, read_files, pruned_files, spilled_local_bytes
FROM system.query.history
WHERE start_time >= current_date() - INTERVAL 1 DAY
ORDER BY total_duration_ms DESC LIMIT 20""")
top.show(truncate=False)
