# Create, change keys and optimize
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.silver.events (event_id STRING, user_id STRING, event_date DATE, country STRING)
CLUSTER BY (event_date, user_id)""")
spark.sql("ALTER TABLE main.silver.events CLUSTER BY (country, event_date)")
spark.sql("OPTIMIZE main.silver.events")            # incremental
spark.sql("OPTIMIZE main.silver.events FULL")       # recluster existing data to new keys
