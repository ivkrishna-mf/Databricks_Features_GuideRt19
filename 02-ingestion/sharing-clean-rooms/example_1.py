# Provider: share a table with history
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("CREATE SHARE IF NOT EXISTS retail_share")
spark.sql("ALTER SHARE retail_share ADD TABLE main.gold.daily_sales WITH HISTORY")
spark.sql("CREATE RECIPIENT partner_co USING ID 'aws:us-west-2:19a8...'")   # D2D identifier
spark.sql("GRANT SELECT ON SHARE retail_share TO RECIPIENT partner_co")
