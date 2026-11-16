# Replace a slice and evolve the schema on write
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
corrected = spark.table("main.staging.orders_2026_11_15")
corrected.createOrReplaceTempView("corrected")
spark.sql("""
INSERT INTO main.silver.orders REPLACE USING (order_date)
SELECT * FROM corrected""")

(new_rows.writeTo("main.silver.orders")
    .withSchemaEvolution()     # DataFrame writer schema evolution (Runtime 19)
    .append())
spark.sql("SET PATH = main.fn, system.builtin")   # unqualified function names resolve in main.fn first
