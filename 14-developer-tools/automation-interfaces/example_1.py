# Python SDK: create a job and run it
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
w = WorkspaceClient()        # reads profile or env vars

job = w.jobs.create(name="adhoc-backfill", tasks=[
    jobs.Task(task_key="main",
              notebook_task=jobs.NotebookTask(notebook_path="/Workspace/Shared/backfill",
                                              base_parameters={"start": "2026-01-01"}))])
run = w.jobs.run_now(job_id=job.job_id).result()      # waits until done
print(run.state.result_state)
