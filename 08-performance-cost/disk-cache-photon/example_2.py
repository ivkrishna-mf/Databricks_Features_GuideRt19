# Make data skipping work for you
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Filters on clustered columns with literal values prune files
fast = spark.table("main.silver.events").where("event_date = '2026-11-01' AND country = 'DE'")
# A function on the column hides it from file statistics
slow = spark.table("main.silver.events").where("date_format(event_date, 'yyyy-MM') = '2026-11'")
fast.explain("formatted")
