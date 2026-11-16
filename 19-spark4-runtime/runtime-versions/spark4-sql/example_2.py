# Pipe syntax and a case-insensitive collation
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
FROM main.silver.orders
|> WHERE order_date >= DATE'2026-10-01'
|> AGGREGATE SUM(amount) AS revenue GROUP BY country
|> ORDER BY revenue DESC
|> LIMIT 10""").show()

spark.sql("CREATE TABLE IF NOT EXISTS main.ref.cities (name STRING COLLATE UTF8_LCASE)")
spark.sql("SELECT * FROM main.ref.cities WHERE name = 'PARIS'").show()   # matches 'Paris'
