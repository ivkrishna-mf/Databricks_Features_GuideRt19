# Delete target rows that left the source
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
MERGE INTO main.silver.products t
USING main.staging.products_snapshot s ON t.sku = s.sku
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE""")
