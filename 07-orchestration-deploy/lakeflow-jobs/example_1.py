# Pass a value between tasks and branch on it
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Task "check_source"
rows = spark.table("main.bronze.orders").where("ingest_date = current_date()").count()
dbutils.jobs.taskValues.set(key="row_count", value=rows)

# If/else condition task: {{tasks.check_source.values.row_count}} > 0
# Task "transform" (runs on the true branch)
n = dbutils.jobs.taskValues.get(taskKey="check_source", key="row_count", debugValue=0)
run_date = dbutils.widgets.get("run_date")          # from {{job.parameters.run_date}}
