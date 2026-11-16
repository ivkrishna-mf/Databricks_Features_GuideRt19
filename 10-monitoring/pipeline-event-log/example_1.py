# Expectation results per dataset
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
q = spark.sql("""
SELECT origin.flow_name AS dataset, e.name AS expectation,
       SUM(e.passed_records) AS passed, SUM(e.failed_records) AS failed
FROM (
  SELECT origin, explode(from_json(details:flow_progress.data_quality.expectations,
         'array<struct<name:string,dataset:string,passed_records:bigint,failed_records:bigint>>')) AS e
  FROM event_log(TABLE(main.silver.silver_orders))
  WHERE event_type = 'flow_progress')
GROUP BY 1, 2""")
q.show(truncate=False)
