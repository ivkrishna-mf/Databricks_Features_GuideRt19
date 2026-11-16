# Pass DataFrames and values into SQL safely
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
recent = spark.table("main.silver.orders").where("order_date >= '2026-11-01'")
top = spark.sql("""
SELECT customer_id, SUM(amount) AS spend
FROM {orders} WHERE amount > {min_amount}
GROUP BY customer_id ORDER BY spend DESC LIMIT 10""", orders=recent, min_amount=50)
top.show()
