# Widen a column type
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.silver.events SET TBLPROPERTIES ('delta.enableTypeWidening' = 'true')")
spark.sql("ALTER TABLE main.silver.events ALTER COLUMN view_count TYPE BIGINT")
# Streaming readers of a renamed/dropped column table:
s = (spark.readStream.option("schemaTrackingLocation", "/Volumes/main/ops/chk/events_schema")
    .table("main.silver.orders"))
