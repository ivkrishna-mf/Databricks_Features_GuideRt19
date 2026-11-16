# Three-level names and volumes
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = spark.table("main.gold.daily_revenue")
spark.sql("CREATE VOLUME IF NOT EXISTS main.landing.orders")
files = dbutils.fs.ls("/Volumes/main/landing/orders/")
spark.sql("ALTER SCHEMA main.gold OWNER TO `gold_owners`")
