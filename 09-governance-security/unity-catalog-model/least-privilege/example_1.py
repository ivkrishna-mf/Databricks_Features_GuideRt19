# Service principal that can write one schema
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
sp = "`sp-orders-pipeline`"
spark.sql(f"GRANT USE CATALOG ON CATALOG main TO {sp}")
spark.sql(f"GRANT USE SCHEMA, CREATE TABLE, MODIFY, SELECT ON SCHEMA main.silver_orders TO {sp}")
spark.sql(f"GRANT USE SCHEMA, SELECT ON SCHEMA main.bronze_orders TO {sp}")
spark.sql("REVOKE ALL PRIVILEGES ON SCHEMA main.silver_orders FROM `developers`")
