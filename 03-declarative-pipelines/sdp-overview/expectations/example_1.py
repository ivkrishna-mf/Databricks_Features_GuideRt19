# Rules as a dictionary: drop bad rows
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
rules = {"valid_id": "order_id IS NOT NULL",
         "positive_amount": "amount > 0",
         "known_currency": "currency IN ('USD','EUR','GBP')"}

@dp.table(name="silver_orders")
@dp.expect_all_or_drop(rules)
def silver_orders():
    return spark.readStream.table("bronze_orders")
