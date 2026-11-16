# Deep clone as an incremental backup
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Rerunning copies only files added since the last run
spark.sql("CREATE OR REPLACE TABLE backup.silver.orders DEEP CLONE main.silver.orders")
