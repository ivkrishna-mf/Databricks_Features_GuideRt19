# Stream-static enrichment
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
orders = spark.readStream.table("main.silver.orders")
customers = spark.read.table("main.silver.customers")     # re-read each micro-batch
enriched = orders.join(customers, "customer_id", "left")
