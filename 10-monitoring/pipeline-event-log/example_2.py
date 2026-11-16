# Errors and update durations
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
log = spark.sql("SELECT * FROM event_log('<pipeline-id>')")
log.where("level = 'ERROR'").select("timestamp", "message", "error").show(truncate=False)
(log.where("event_type = 'update_progress'")
    .selectExpr("origin.update_id", "details:update_progress.state::string AS state", "timestamp")
    .show())
