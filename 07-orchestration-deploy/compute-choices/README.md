# Choosing compute

Available since ~2023 · DE Professional exam: S1, S5

## What it is

Compute choice is a cost and isolation decision. Serverless starts in seconds and needs no sizing. Job compute is created for a run and terminated after. All-purpose compute is for interactive work and costs more per unit.

## How it flows

1. **Workload**: Interactive, scheduled job, pipeline or SQL.
2. **Serverless available and suitable?**: Use it.
3. **Needs custom runtime, init scripts or special instances?**: Classic job compute.
4. **Set environment**: Dependencies in a serverless environment or cluster libraries.
5. **Run and observe**: Use system tables to check cost.

```
[Workload] --> [Serverless available and suitable?] --> [Needs custom runtime, init scripts or special instances?] --> [Set environment] --> [Run and observe]
```

## When to choose it

**Choose it when**

- Serverless: variable or bursty load, small teams, fast start.
- Classic: stable heavy jobs you have tuned, or features serverless lacks.

**Pick something else when**

- Running scheduled jobs on an all-purpose cluster.
- Dedicated access mode when several users share a cluster: use standard access mode.

## Options

| Compute | Choose when | Watch out |
|---|---|---|
| Serverless jobs and notebooks | Default for most Python and SQL work | Performance optimized mode starts faster and costs more; standard mode is cheaper with a longer startup |
| Classic job compute | Custom Spark configs, init scripts, GPUs, private networking needs | Startup minutes; you size and tune it |
| All-purpose compute | Development and exploration | Most expensive way to run a schedule |
| SQL warehouse (serverless) | SQL tasks, dashboards, alerts | Not for Python |
| Pipeline compute | Managed by the pipeline, serverless or classic | Edition and mode affect features and price |

## Senior engineer verdict

> I start serverless and move a job to classic compute only with a number that justifies it. On serverless I set the environment explicitly, choose standard performance mode for anything not latency-bound, and turn off automatic retries for tasks that are not idempotent.

## Examples

### 1. Serverless job with an environment, from Python

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs, compute
w = WorkspaceClient()
w.jobs.create(name="daily_enrich", performance_target=jobs.PerformanceTarget.STANDARD,
    environments=[jobs.JobEnvironment(environment_key="default",
        spec=compute.Environment(environment_version="4", dependencies=["rapidfuzz==3.9.7"]))],
    tasks=[jobs.Task(task_key="enrich", environment_key="default",
        spark_python_task=jobs.SparkPythonTask(python_file="/Workspace/Shared/enrich.py"))])
```

### 2. Classic cluster sized from helpers

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute
w = WorkspaceClient()
cluster = w.clusters.create_and_wait(
    cluster_name="etl-classic",
    spark_version=w.clusters.select_spark_version(latest=True, long_term_support=True),
    node_type_id=w.clusters.select_node_type(local_disk=True, min_memory_gb=32),
    autoscale=compute.AutoScale(min_workers=2, max_workers=8),
    autotermination_minutes=30,
    data_security_mode=compute.DataSecurityMode.USER_ISOLATION)
print(cluster.cluster_id, cluster.spark_version)
```

### 3. Serverless job task with an environment and standard mode

File: [`example_3.yml`](example_3.yml)

```yaml
resources:
  jobs:
    daily_enrich:
      performance_target: STANDARD           # PERFORMANCE_OPTIMIZED for faster start
      environments:
        - environment_key: default
          spec:
            environment_version: "4"
            dependencies: ["./dist/*.whl", "rapidfuzz==3.9.7"]
      tasks:
        - task_key: enrich
          environment_key: default
          spark_python_task: { python_file: ../src/enrich.py }
          disable_auto_optimization: true    # no automatic retries on serverless
```

### 4. Classic job cluster when you need control

File: [`example_4.yml`](example_4.yml)

```yaml
job_clusters:
        - job_cluster_key: etl
          new_cluster:
            spark_version: 19.x-scala2.13     # pick the exact key your workspace lists
            node_type_id: i3.2xlarge
            data_security_mode: USER_ISOLATION   # standard access mode
            autoscale: { min_workers: 2, max_workers: 8 }
            spark_conf: { "spark.sql.shuffle.partitions": "auto" }
```

## Traps and gotchas

- Standard (formerly shared) and dedicated (formerly single user) access modes both support Unity Catalog; no-isolation shared does not.
- High memory is a notebook task setting on serverless for memory-heavy driver work.
- Serverless ignores most Spark configs.
