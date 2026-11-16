# Rename and drop without rewriting data
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name')")
spark.sql("ALTER TABLE main.silver.orders RENAME COLUMN cust_no TO customer_id")
spark.sql("ALTER TABLE main.silver.orders DROP COLUMN legacy_flag")
