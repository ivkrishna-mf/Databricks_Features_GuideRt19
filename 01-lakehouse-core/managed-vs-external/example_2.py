# External table on an external location
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.raw.partner_feed (id STRING, body STRING)
LOCATION 's3://partner-bucket/feed/'""")
# Dropping it removes metadata only; files remain in the bucket
spark.sql("DROP TABLE main.raw.partner_feed")
