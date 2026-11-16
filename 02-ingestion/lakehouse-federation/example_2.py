# Join federated and lakehouse data
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
accounts = spark.table("crm.public.accounts").where("region = 'EMEA'")   # pushed down
orders = spark.table("main.gold.fact_orders")
orders.join(accounts, "account_id").groupBy("segment").sum("amount").show()
