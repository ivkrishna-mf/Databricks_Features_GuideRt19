# For each and an if/else branch with the Python SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
w = WorkspaceClient()
w.jobs.create(name="nightly_load", tasks=[
    jobs.Task(task_key="list_tables", notebook_task=jobs.NotebookTask(notebook_path="/Workspace/Shared/list_tables")),
    jobs.Task(task_key="has_work", depends_on=[jobs.TaskDependency(task_key="list_tables")],
              condition_task=jobs.ConditionTask(left="{{tasks.list_tables.values.count}}",
                                                op=jobs.ConditionTaskOp.GREATER_THAN, right="0")),
    jobs.Task(task_key="load_each", depends_on=[jobs.TaskDependency(task_key="has_work", outcome="true")],
              for_each_task=jobs.ForEachTask(inputs="{{tasks.list_tables.values.tables}}", concurrency=4,
                  task=jobs.Task(task_key="load_one", notebook_task=jobs.NotebookTask(
                      notebook_path="/Workspace/Shared/load_table", base_parameters={"table": "{{input}}"}))))])
