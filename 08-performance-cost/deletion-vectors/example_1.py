# Enable and delete
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.silver.customers SET TBLPROPERTIES ('delta.enableDeletionVectors' = true)")
spark.sql("DELETE FROM main.silver.customers WHERE customer_id = 'C-1042'")
spark.sql("DESCRIBE HISTORY main.silver.customers").select("operation", "operationMetrics").show(1, False)
