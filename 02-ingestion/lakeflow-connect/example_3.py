# Read the ingested table downstream
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# SCD2 output keeps history with __START_AT and __END_AT
current = (spark.read.table("main.bronze_erp.customers")
    .where("__END_AT IS NULL"))
changes = spark.readStream.option("skipChangeCommits", "true").table("main.bronze_erp.customers")
