# Manual maintenance for an external table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("OPTIMIZE main.raw.partner_feed")
spark.sql("ALTER TABLE main.raw.partner_feed SET TBLPROPERTIES ("
          "'delta.autoOptimize.optimizeWrite' = 'true', 'delta.autoOptimize.autoCompact' = 'true')")
spark.sql("VACUUM main.raw.partner_feed RETAIN 168 HOURS")
