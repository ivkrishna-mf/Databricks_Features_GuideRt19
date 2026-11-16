# Add new columns on append
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
(new_df.write.mode("append")
    .option("mergeSchema", "true")
    .saveAsTable("main.silver.orders"))
