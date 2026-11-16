# Guard a feature by runtime version
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import os
major = int(os.environ.get("DATABRICKS_RUNTIME_VERSION", "0").split(".")[0] or 0)
if major >= 19:
    changes = spark.read.option("readChangeFeed", "true").option("startingVersion", 10).table("main.silver.orders")
else:
    spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
    changes = spark.read.option("readChangeFeed", "true").option("startingVersion", 10).table("main.silver.orders")
