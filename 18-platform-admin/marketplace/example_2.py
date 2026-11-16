# Provider side: prepare a share for a listing
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("CREATE SHARE IF NOT EXISTS public_reference COMMENT 'Listing: retail calendar'")
spark.sql("ALTER SHARE public_reference ADD TABLE main.ref.retail_calendar")
# Then create the listing in the Marketplace provider console and attach the share
