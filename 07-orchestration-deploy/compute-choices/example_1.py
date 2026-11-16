# Serverless job with an environment, from Python
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs, compute
w = WorkspaceClient()
w.jobs.create(name="daily_enrich", performance_target=jobs.PerformanceTarget.STANDARD,
    environments=[jobs.JobEnvironment(environment_key="default",
        spec=compute.Environment(environment_version="4", dependencies=["rapidfuzz==3.9.7"]))],
    tasks=[jobs.Task(task_key="enrich", environment_key="default",
        spark_python_task=jobs.SparkPythonTask(python_file="/Workspace/Shared/enrich.py"))])
