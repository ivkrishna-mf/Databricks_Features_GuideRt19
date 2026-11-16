# Cost per job over the last 30 days
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
cost = spark.sql("""
SELECT u.usage_metadata.job_id AS job_id,
       SUM(u.usage_quantity * p.pricing.default) AS est_cost
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON u.sku_name = p.sku_name AND u.cloud = p.cloud
 AND u.usage_start_time >= p.price_start_time
 AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= current_date() - INTERVAL 30 DAYS
  AND u.usage_metadata.job_id IS NOT NULL
GROUP BY 1 ORDER BY est_cost DESC""")
cost.show(20)
