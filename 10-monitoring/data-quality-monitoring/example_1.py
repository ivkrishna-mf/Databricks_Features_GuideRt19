# Read anomaly detection results
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
issues = spark.sql("""
SELECT *
FROM system.data_quality_monitoring.table_results
WHERE catalog_name = 'main' AND schema_name = 'gold'
ORDER BY event_time DESC
LIMIT 50""")
issues.show(truncate=False)
