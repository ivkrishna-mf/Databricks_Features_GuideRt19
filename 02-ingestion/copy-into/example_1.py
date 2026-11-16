# Idempotent load with schema evolution
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
COPY INTO main.bronze.invoices
FROM '/Volumes/main/landing/invoices/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')""")
