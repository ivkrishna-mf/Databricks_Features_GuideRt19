# Delete across tables from a request list
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
keys = spark.table("main.privacy.erasure_requests").where("status = 'OPEN'").select("customer_id")
keys.createOrReplaceTempView("to_erase")
for t in ["main.bronze.customers", "main.silver.customers", "main.silver.orders"]:
    spark.sql(f"DELETE FROM {t} WHERE customer_id IN (SELECT customer_id FROM to_erase)")
