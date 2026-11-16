# Make the deletion physical
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
for t in ["main.bronze.customers", "main.silver.customers", "main.silver.orders"]:
    spark.sql(f"ALTER TABLE {t} SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 7 days')")
    spark.sql(f"REORG TABLE {t} APPLY (PURGE)")
    spark.sql(f"VACUUM {t}")                 # removes files older than the retention
