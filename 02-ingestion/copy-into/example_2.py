# Force a reload of all files
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
COPY INTO main.bronze.invoices
FROM '/Volumes/main/landing/invoices/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('force' = 'true')""")      # ignores load history: duplicates possible
