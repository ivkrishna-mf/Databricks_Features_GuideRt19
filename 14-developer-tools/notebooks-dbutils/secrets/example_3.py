# Read secrets in Python and SQL
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import requests
key = dbutils.secrets.get(scope="crm", key="api_key")
r = requests.get("https://api.crm.example/v1/accounts", headers={"Authorization": "Bearer " + key}, timeout=30)
print(key)      # prints [REDACTED]

spark.sql("SELECT secret('crm', 'api_key') IS NOT NULL AS has_key").show()
