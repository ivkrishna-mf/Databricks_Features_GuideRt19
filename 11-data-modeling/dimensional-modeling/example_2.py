# Metric view with a governed ratio
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE OR REPLACE VIEW main.gold.sales_metrics
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
source: main.gold.fact_orders
dimensions:
  - name: order_month
    expr: date_trunc('MONTH', order_date)
measures:
  - name: revenue
    expr: SUM(amount)
  - name: avg_order_value
    expr: SUM(amount) / COUNT(DISTINCT order_id)
$$""")
spark.sql("""
SELECT order_month, MEASURE(revenue), MEASURE(avg_order_value)
FROM main.gold.sales_metrics GROUP BY order_month""").show()
