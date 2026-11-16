# Query profile, Spark UI and common bottlenecks

**Major feature** · Available since ~2020 · DE Professional exam: S5, S8

## What it is

The query profile (SQL warehouses and serverless) and the Spark UI (classic compute) show where time goes: scan, shuffle, join, spill, skew. Adaptive Query Execution fixes much at runtime by coalescing partitions, switching join strategies and splitting skewed partitions.

## How it flows

1. **Slow query**: Open the query profile or the SQL tab of the Spark UI.
2. **Scan**: Files read against files pruned. Low pruning means clustering or filter problems.
3. **Join**: Broadcast or sort-merge. Row explosion means bad keys.
4. **Shuffle**: Size, spill to disk, one task far slower than the rest (skew).
5. **Fix**: Clustering, filter rewrite, broadcast, more partitions or memory, salting.

```
[Slow query] --> [Scan] --> [Join] --> [Shuffle] --> [Fix]
```

## When to choose it

**Choose it when**

- Any time a job gets slower or more expensive: look before changing configs.

## Symptom to cause

| What you see | Likely cause | Fix |
|---|---|---|
| Most files read, few rows returned | No data skipping on the filter column | Cluster by that column; avoid functions on it |
| One task takes most of the stage time | Skewed key | Let AQE skew join work, filter nulls, salt, or broadcast |
| Spill (memory and disk) in the stage | Partitions too large | More shuffle partitions (or auto), larger workers |
| Sort-merge join with a small table | Statistics missing or threshold too low | ANALYZE, broadcast hint |
| Many tiny tasks and files | Too many partitions or small files | OPTIMIZE, optimized writes, coalesce |
| Driver out of memory | `collect`, `toPandas`, huge broadcast | Keep data distributed |
| Executor lost, exit code 137 | Out of memory on a worker | Fewer cores per memory, fix skew, avoid giant UDF batches |

## Senior engineer verdict

> I read the profile from the scan upward. If the scan reads the whole table, nothing downstream will save the query. Cluster logs split by purpose: driver logs for your own errors and stack traces, executor logs for task failures, event logs for cluster lifecycle such as spot loss.

## Examples

### 1. Read the plan and fix a skewed join

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
orders = spark.table("main.silver.orders").where("customer_id IS NOT NULL")   # null keys skew
dims = spark.table("main.silver.customers")
joined = orders.join(dims.hint("broadcast"), "customer_id")
joined.explain("formatted")       # look for BroadcastHashJoin and PushedFilters
```

### 2. Find the most expensive queries from system tables

File: [`example_2.py`](example_2.py)

```python
top = spark.sql("""
SELECT statement_id, executed_by, total_duration_ms, read_files, pruned_files, spilled_local_bytes
FROM system.query.history
WHERE start_time >= current_date() - INTERVAL 1 DAY
ORDER BY total_duration_ms DESC LIMIT 20""")
top.show(truncate=False)
```

## Traps and gotchas

- A broadcast join has no shuffle on the large side; a sort-merge join shuffles both.
- Spill means partitions do not fit in memory; it is not fixed by caching.
- In the Spark UI, skew shows as a large gap between median and max task duration or shuffle read size.
