# Physically remove soft-deleted rows
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("REORG TABLE main.silver.customers APPLY (PURGE)")      # rewrite files that have deletion vectors
spark.sql("VACUUM main.silver.customers RETAIN 168 HOURS")       # then drop old files after 7 days
