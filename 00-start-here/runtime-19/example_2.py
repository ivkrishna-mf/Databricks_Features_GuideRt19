# INSERT REPLACE for idempotent reprocessing
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.table("main.staging.events_fix").createOrReplaceTempView("fix")
spark.sql("INSERT INTO main.silver.events REPLACE USING (event_date) SELECT * FROM fix")
spark.sql("DESCRIBE HISTORY main.silver.events").select("version", "operation").show(3)
