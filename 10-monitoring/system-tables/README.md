# System tables

**Major feature** · Available since ~2023 · DE Professional exam: S4

## What it is

Read-only tables in the `system` catalog that record how the account is used: billing, compute, jobs and pipelines, queries, audit events and lineage. They are the supported source for cost and operations reporting.

## How it flows

1. **Activity happens**: A job runs, a user queries, a cluster starts.
2. **Recorded**: In the matching system schema.
3. **Query**: Join usage with prices, jobs with run timelines.
4. **Dashboard**: Cost by job, failures by team.
5. **Alert**: A SQL alert on the same query.

```
[Activity happens] --> [Recorded] --> [Query] --> [Dashboard] --> [Alert]
```

## When to choose it

**Choose it when**

- Cost attribution, SLA reporting, audits.

**Pick something else when**

- Scraping the UI or building your own run log.

## Which table answers which question

| Question | Table |
|---|---|
| What did we spend, by job or tag? | `system.billing.usage` joined to `system.billing.list_prices` |
| Which jobs failed or ran long? | `system.lakeflow.job_run_timeline`, `system.lakeflow.job_task_run_timeline` |
| Job and pipeline definitions over time | `system.lakeflow.jobs`, `system.lakeflow.job_tasks`, `system.lakeflow.pipelines` |
| Cluster configuration and utilization | `system.compute.clusters`, `system.compute.node_timeline` |
| Who accessed or changed what? | `system.access.audit` |
| What feeds what? | `system.access.table_lineage`, `system.access.column_lineage` |
| Slow or expensive queries | `system.query.history` |

## Senior engineer verdict

> Usage alone is in DBUs; multiply by list prices for an estimate in currency and attribute with `usage_metadata.job_id` and custom tags. I tag every job and cluster with team and cost center, otherwise the cost report ends in 'unknown'.

## Examples

### 1. Cost per job over the last 30 days

File: [`example_1.py`](example_1.py)

```python
cost = spark.sql("""
SELECT u.usage_metadata.job_id AS job_id,
       SUM(u.usage_quantity * p.pricing.default) AS est_cost
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON u.sku_name = p.sku_name AND u.cloud = p.cloud
 AND u.usage_start_time >= p.price_start_time
 AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= current_date() - INTERVAL 30 DAYS
  AND u.usage_metadata.job_id IS NOT NULL
GROUP BY 1 ORDER BY est_cost DESC""")
cost.show(20)
```

### 2. Failed job runs and an audit question

File: [`example_2.py`](example_2.py)

```python
failed = spark.sql("""
SELECT job_id, run_id, result_state, period_start_time
FROM system.lakeflow.job_run_timeline
WHERE result_state IN ('FAILED', 'TIMED_OUT')
  AND period_start_time >= current_timestamp() - INTERVAL 24 HOURS""")

grants = (spark.table("system.access.audit")
    .where("service_name = 'unityCatalog' AND action_name = 'updatePermissions'")
    .select("event_time", "user_identity.email", "request_params"))
```

## Traps and gotchas

- System tables must be enabled per schema by an admin and need grants to read.
- Billing data is account-wide; filter by workspace when needed.
- Data arrives with a delay; they are not for second-level alerting.
