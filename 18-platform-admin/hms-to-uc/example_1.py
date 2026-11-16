# Upgrade external tables in place with SYNC
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("SYNC SCHEMA main.sales FROM hive_metastore.sales DRY RUN").show(truncate=False)
spark.sql("SYNC SCHEMA main.sales FROM hive_metastore.sales")
spark.sql("SYNC TABLE main.sales.orders FROM hive_metastore.sales.orders")   # single table
