# Alerts and notifications

Available since ~2020 · DE Professional exam: S4

## What it is

A SQL alert runs a query on a schedule, checks a condition and notifies a destination such as email, Slack, PagerDuty or a webhook. Jobs and pipelines also send their own notifications on start, success, failure and when a run exceeds a duration.

## How it flows

1. **Scheduled query**: On a SQL warehouse.
2. **Condition**: Value compared with a threshold.
3. **State change**: OK to triggered.
4. **Notify**: Destination receives the message.
5. **Act**: A person or a job responds.

```
[Scheduled query] --> [Condition] --> [State change] --> [Notify] --> [Act]
```

## When to choose it

**Choose it when**

- Anything someone must act on.

**Pick something else when**

- Alerts nobody owns. Each alert needs a destination and a runbook.

## What to alert on

| Signal | Source |
|---|---|
| Data quality: failed expectations, anomalies in freshness or volume | Pipeline event log, data quality monitoring |
| Business metric out of range | Metric view or gold table |
| Cost spike | `system.billing.usage` |
| Slow or queued queries | `system.query.history`, warehouse events |
| Security: privilege changes, failed logins | `system.access.audit` |
| Job failure or late run | Job notifications, duration thresholds |
| AI agent quality | Evaluation and trace tables |

## Senior engineer verdict

> Failure notifications belong on the job itself; SQL alerts are for conditions inside the data. I alert on freshness more than on failure, because a pipeline that succeeds with zero rows is the incident nobody gets paged for.

## Examples

### 1. Freshness check query behind an alert

File: [`example_1.py`](example_1.py)

```python
fresh = spark.sql("""
SELECT timestampdiff(MINUTE, max(ingested_at), current_timestamp()) AS minutes_stale
FROM main.silver.orders""")
# Alert condition in the UI or API: minutes_stale > 90
```

### 2. Fail the task when data is stale, so job alerts fire

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F
stale = (spark.table("main.silver.orders")
    .agg(F.expr("timestampdiff(MINUTE, max(ingested_at), current_timestamp())").alias("m"))
    .first()["m"])
if stale is None or stale > 90:
    raise RuntimeError(f"main.silver.orders is {stale} minutes stale")   # on_failure notification
```

### 3. Job notifications and duration threshold in a bundle

File: [`example_3.yml`](example_3.yml)

```yaml
resources:
  jobs:
    nightly_load:
      email_notifications:
        on_failure: [data-oncall@acme.com]
        on_duration_warning_threshold_exceeded: [data-oncall@acme.com]
      health:
        rules:
          - metric: RUN_DURATION_SECONDS
            op: GREATER_THAN
            value: 3600
      webhook_notifications:
        on_failure: [{ id: "<notification-destination-id>" }]
```

## Traps and gotchas

- An alert evaluates the first row of the query result unless configured otherwise.
- Alerts run on SQL warehouses.
