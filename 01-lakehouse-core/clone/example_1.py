# Shallow clone for a test run
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE OR REPLACE TABLE dev.sandbox.orders_test
SHALLOW CLONE main.silver.orders VERSION AS OF 230""")
