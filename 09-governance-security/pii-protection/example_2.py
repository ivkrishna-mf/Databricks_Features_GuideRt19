# Tokenization with a vault table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
new_ids = (spark.table("main.bronze.customers").select("customer_id").distinct()
    .join(spark.table("main.vault.customer_tokens"), "customer_id", "left_anti")
    .withColumn("token", F.expr("uuid()")))
new_ids.write.mode("append").saveAsTable("main.vault.customer_tokens")     # restricted schema

tokenized = (spark.table("main.bronze.orders")
    .join(spark.table("main.vault.customer_tokens"), "customer_id")
    .drop("customer_id"))
