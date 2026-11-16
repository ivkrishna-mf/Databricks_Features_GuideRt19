# Monitoring with REST API, CLI, SDK and streaming metrics

Available since ~2016 · DE Professional exam: S4

## What it is

Everything in the Jobs and Pipelines UI is available programmatically. The REST API is the base; the CLI and the Python SDK wrap it. Streaming queries expose progress metrics through `lastProgress` and StreamingQueryListener.

## How it flows

1. **Trigger or list**: Run a job, list runs.
2. **Poll**: Run state and task states.
3. **Inspect**: Errors, durations, output.
4. **Act**: Repair, cancel or notify.
5. **Record**: Send metrics to your observability tool.

```
[Trigger or list] --> [Poll] --> [Inspect] --> [Act] --> [Record]
```

## When to choose it

**Choose it when**

- External orchestrators, CI checks, custom dashboards.

**Pick something else when**

- Polling tight loops; use the wait helpers or webhooks.

## Senior engineer verdict

> For a stream I watch three numbers: input rate against processing rate, batch duration against trigger interval, and state rows. If input stays above processing, the backlog grows and no amount of waiting fixes it.

## Examples

### 1. Run a job, wait, and repair on failure

File: [`example_1.py`](example_1.py)

```python
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
```

### 2. Streaming progress metrics

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql.streaming import StreamingQueryListener
class Lag(StreamingQueryListener):
    def onQueryStarted(self, e): pass
    def onQueryTerminated(self, e): pass
    def onQueryProgress(self, e):
        p = e.progress
        print(p.name, p.batchId, p.numInputRows, p.inputRowsPerSecond, p.processedRowsPerSecond)
spark.streams.addListener(Lag())
# Ad hoc: query.lastProgress["durationMs"], query.lastProgress["stateOperators"]
```

### 3. CLI equivalents

File: [`example_3.sh`](example_3.sh)

```bash
databricks jobs list-runs --job-id 123 --limit 5
databricks jobs get-run 456789
databricks jobs repair-run 456789 --rerun-all-failed-tasks
databricks pipelines list-pipeline-events <pipeline-id>
```

## Traps and gotchas

- Repair is an API call on a run id, not a new run.
- `processedRowsPerSecond` below `inputRowsPerSecond` over time means the stream is falling behind.
