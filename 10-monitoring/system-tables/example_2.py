# Failed job runs and an audit question
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
failed = spark.sql("""
SELECT job_id, run_id, result_state, period_start_time
FROM system.lakeflow.job_run_timeline
WHERE result_state IN ('FAILED', 'TIMED_OUT')
  AND period_start_time >= current_timestamp() - INTERVAL 24 HOURS""")

grants = (spark.table("system.access.audit")
    .where("service_name = 'unityCatalog' AND action_name = 'updatePermissions'")
    .select("event_time", "user_identity.email", "request_params"))
