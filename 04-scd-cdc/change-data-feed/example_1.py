# Enable and read changes in batch
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.silver.customers SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

changes = (spark.read
    .option("readChangeFeed", "true")
    .option("startingVersion", 15).option("endingVersion", 20)
    .table("main.silver.customers"))
changes.where("_change_type IN ('insert', 'update_postimage', 'delete')").show()
