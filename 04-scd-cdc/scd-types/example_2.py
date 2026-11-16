# Current view over the same dimension (as-is reporting)
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE OR REPLACE VIEW main.gold.dim_customer_current AS
SELECT * EXCEPT (__START_AT, __END_AT)
FROM main.gold.dim_customer_history
WHERE __END_AT IS NULL""")
