# Lakeflow Jobs

**Major feature** · Available since ~2015 · DE Professional exam: S1, S8

## What it is

Jobs orchestrate tasks as a graph: notebooks, Python scripts and wheels, SQL, pipelines, dbt, other jobs. Tasks pass small values to each other, run conditionally, loop over inputs, and can be repaired after a failure without rerunning what succeeded.

## How it flows

1. **Trigger**: Schedule, file arrival, table update, continuous, or API.
2. **Tasks run**: In dependency order, with retries.
3. **Control flow**: If/else branches on a value; For each loops over a list.
4. **Failure**: Notifications fire; downstream tasks follow their Run if rule.
5. **Repair run**: Rerun only failed and skipped tasks, optionally with new parameters.

```
[Trigger] --> [Tasks run] --> [Control flow] --> [Failure] --> [Repair run]
```

## When to choose it

**Choose it when**

- Any production schedule, especially mixing pipelines with imperative steps.
- Fan-out over a list of tables, regions or dates.

**Pick something else when**

- Expressing table-to-table dependencies by hand when a pipeline would infer them.

## Control flow and recovery

| Feature | What it does |
|---|---|
| Task values | `dbutils.jobs.taskValues.set` in one task, `{{tasks.t.values.k}}` in the next |
| Job parameters | `{{job.parameters.name}}`, overridable per run and on repair |
| If/else condition task | Branches on a comparison of parameters or task values |
| For each task | Runs a nested task per item of an array, with a concurrency limit |
| Run if | All succeeded (default), at least one succeeded, none failed, all done, at least one failed, all failed |
| Repair run | Reruns failed and dependent tasks in the same job run; successful tasks are kept |

## Senior engineer verdict

> I keep jobs thin: orchestration and parameters only, with logic in pipelines and tested Python packages. For recovery I rely on repair runs rather than rerunning the job, which only works if every task is idempotent.

## Examples

### 1. Pass a value between tasks and branch on it

File: [`example_1.py`](example_1.py)

```python
# Task "check_source"
rows = spark.table("main.bronze.orders").where("ingest_date = current_date()").count()
dbutils.jobs.taskValues.set(key="row_count", value=rows)

# If/else condition task: {{tasks.check_source.values.row_count}} > 0
# Task "transform" (runs on the true branch)
n = dbutils.jobs.taskValues.get(taskKey="check_source", key="row_count", debugValue=0)
run_date = dbutils.widgets.get("run_date")          # from {{job.parameters.run_date}}
```

### 2. For each and an if/else branch with the Python SDK

File: [`example_2.py`](example_2.py)

```python
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
```

### 3. For each loop and a conditional task in a bundle

File: [`example_3.yml`](example_3.yml)

```yaml
resources:
  jobs:
    nightly_load:
      name: nightly_load
      parameters:
        - name: run_date
          default: "{{job.start_time.iso_date}}"
      tasks:
        - task_key: list_tables
          notebook_task: { notebook_path: ../src/list_tables.py }
        - task_key: load_each
          depends_on: [{ task_key: list_tables }]
          for_each_task:
            inputs: "{{tasks.list_tables.values.tables}}"
            concurrency: 4
            task:
              task_key: load_one
              notebook_task:
                notebook_path: ../src/load_table.py
                base_parameters: { table: "{{input}}" }
        - task_key: notify_failure
          depends_on: [{ task_key: load_each }]
          run_if: AT_LEAST_ONE_FAILED
          notebook_task: { notebook_path: ../src/notify.py }
```

## Traps and gotchas

- Repair keeps the same run id and reruns only failed, skipped and downstream tasks.
- Task values are for small values, not DataFrames.
- A continuous trigger restarts the job after it ends or fails; it is not the same as a continuous pipeline.
