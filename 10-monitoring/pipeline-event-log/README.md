# Pipeline event log

Available since ~2021 · DE Professional exam: S4

## What it is

Every Lakeflow pipeline writes an event log: update progress, flow metrics, expectation results, lineage, errors and cluster events. You query it with the `event_log()` function or publish it as a table.

## How it flows

1. **Pipeline update**: Starts.
2. **Events emitted**: flow_progress, update_progress, user_action and more.
3. **Details column**: JSON with metrics and expectation counts.
4. **Query**: Parse the JSON for quality and throughput.
5. **Dashboard or alert**: For example dropped rows above a threshold.

```
[Pipeline update] --> [Events emitted] --> [Details column] --> [Query] --> [Dashboard or alert]
```

## When to choose it

**Choose it when**

- Data quality reporting.
- Debugging a failed or slow update.

**Pick something else when**

- Parsing driver logs for numbers the event log already has.

## Senior engineer verdict

> I publish the event log to a table in an ops schema and put one dashboard on top: rows written, rows dropped by expectation, update duration, backlog. That is the health view the team opens first.

## Examples

### 1. Expectation results per dataset

File: [`example_1.py`](example_1.py)

```python
q = spark.sql("""
SELECT origin.flow_name AS dataset, e.name AS expectation,
       SUM(e.passed_records) AS passed, SUM(e.failed_records) AS failed
FROM (
  SELECT origin, explode(from_json(details:flow_progress.data_quality.expectations,
         'array<struct<name:string,dataset:string,passed_records:bigint,failed_records:bigint>>')) AS e
  FROM event_log(TABLE(main.silver.silver_orders))
  WHERE event_type = 'flow_progress')
GROUP BY 1, 2""")
q.show(truncate=False)
```

### 2. Errors and update durations

File: [`example_2.py`](example_2.py)

```python
log = spark.sql("SELECT * FROM event_log('<pipeline-id>')")
log.where("level = 'ERROR'").select("timestamp", "message", "error").show(truncate=False)
(log.where("event_type = 'update_progress'")
    .selectExpr("origin.update_id", "details:update_progress.state::string AS state", "timestamp")
    .show())
```

## Traps and gotchas

- Expectation metrics live in `flow_progress` events under `details:flow_progress.data_quality`.
- Only the pipeline owner can query `event_log()` directly; publish it or create a view to share.
