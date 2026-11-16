# ai_query with errors returned as data
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
scored = spark.sql("""
SELECT ticket_id,
       ai_query('databricks-meta-llama-3-3-70b-instruct',
                concat('Extract the product name from: ', body),
                failOnError => false) AS r
FROM main.silver.tickets""")
ok = scored.selectExpr("ticket_id", "r.result AS product", "r.errorMessage AS error")
