# Run a job, wait, and repair on failure
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunResultState
w = WorkspaceClient()
run = w.jobs.run_now(job_id=123, job_parameters={"run_date": "2026-11-15"}).result()
print(run.state.result_state)
for t in run.tasks:
    print(t.task_key, t.state.result_state)
if run.state.result_state == RunResultState.FAILED:
    w.jobs.repair_run(run_id=run.run_id, rerun_all_failed_tasks=True,
                      job_parameters={"run_date": "2026-11-15"})
