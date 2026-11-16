# Grants that inherit
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("GRANT USE CATALOG ON CATALOG main TO `data_analysts`")
spark.sql("GRANT USE SCHEMA, SELECT ON SCHEMA main.gold TO `data_analysts`")   # all current and future tables
spark.sql("SHOW GRANTS ON SCHEMA main.gold").show(truncate=False)
