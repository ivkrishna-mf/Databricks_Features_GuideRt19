# Read a Delta table that also receives updates
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
stream = (spark.readStream
    .option("skipChangeCommits", "true")       # ignore commits that rewrite existing rows
    .option("maxFilesPerTrigger", 200)
    .table("main.silver.customers"))
