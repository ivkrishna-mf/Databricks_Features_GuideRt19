# Streaming table or materialized view

**Major feature** · Available since ~2023 · DE Professional exam: S1, S9 · Part of [Lakeflow Spark Declarative Pipelines (SDP)](../README.md)

## What it is

A streaming table processes each input row once, in arrival order, and keeps what it wrote. A materialized view stores the result of a query and is refreshed so that it always matches that query over the current source data.

## How it flows

1. **New source data**: Rows are appended, or existing rows change.
2. **Streaming table**: Reads only new rows from its checkpoint and appends or applies CDC.
3. **Materialized view**: Refresh recomputes, incrementally where the engine can.
4. **Result**: Streaming table: history of processing. Materialized view: correct answer as of the refresh.

```
[New source data] --> [Streaming table] --> [Materialized view] --> [Result]
```

## When to choose it

**Choose it when**

- Streaming table: high-volume append-only data, low latency, or data that the source will not keep.
- Materialized view: aggregates, joins with dimensions that change, or results that must be exactly right after source corrections.

**Pick something else when**

- Streaming table over a source that is updated in place, unless you read its change feed or skip change commits.
- Materialized view for sub-minute freshness on a large table.

## Decision table

| Question | Streaming table | Materialized view |
|---|---|---|
| Source behavior | Append-only (files, Kafka, CDC feed) | Any, including updates and deletes |
| Latency | Seconds to minutes, can run continuously | As fresh as the last refresh |
| Cost | Low: only new data | Low when refresh is incremental (serverless), higher on full recompute |
| Changing the logic | Old rows keep old logic unless you full refresh | Next refresh applies the new logic to everything |
| Typical layer | Bronze and silver, SCD targets | Gold aggregates and joins |

## Senior engineer verdict

> My rule: ingest with streaming tables, serve with materialized views. If someone asks for an aggregate as a streaming table, I ask what should happen when late or corrected data arrives. If the answer is 'the number should fix itself', it is a materialized view.

## Examples

### 1. Streaming table from an append-only source

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp

@dp.table(name="silver_events", table_properties={"pipelines.reset.allowed": "false"})
def silver_events():
    return (spark.readStream.table("bronze_events")
        .where("event_type IS NOT NULL"))
```

### 2. Materialized view over data that gets corrected

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_customer_ltv")
def gold_customer_ltv():
    orders = spark.read.table("silver_orders")
    customers = spark.read.table("silver_customers")     # SCD1, rows change
    return (orders.join(customers, "customer_id")
        .groupBy("customer_id", "segment")
        .agg(F.sum("amount").alias("lifetime_value")))
```

## Traps and gotchas

- A full refresh of a streaming table truncates and reprocesses. If the source no longer has the data (Kafka retention, deleted files) it is lost. `pipelines.reset.allowed` = false protects the table.
- Incremental refresh of materialized views needs serverless pipelines; otherwise expect a full recompute.
- Stream-static join in a streaming table: a later change in the static side does not update rows already written.
