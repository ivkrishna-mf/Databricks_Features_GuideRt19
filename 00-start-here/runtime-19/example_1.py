# Read row-level changes without enabling CDF per table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Runtime 19+: row tracking on, changes are computed at query time
spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES ('delta.enableRowTracking' = 'true')")

changes = (spark.read
    .option("readChangeFeed", "true")
    .option("startingVersion", 120)
    .table("main.silver.orders"))
changes.groupBy("_change_type").count().show()
