# Recipient: mount and stream the share
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("CREATE CATALOG partner_retail USING SHARE acme.retail_share")
stream = (spark.readStream
    .option("readChangeFeed", "true")
    .table("partner_retail.gold.daily_sales"))
