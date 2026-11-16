# Copy a managed table and install UCX
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("CREATE TABLE main.sales.customers DEEP CLONE hive_metastore.sales.customers")
spark.sql("ALTER TABLE hive_metastore.sales.customers SET TBLPROPERTIES ('upgraded_to' = 'main.sales.customers')")
# Shell, on your machine:
#   databricks labs install ucx
#   databricks labs ucx ensure-assessment-run
