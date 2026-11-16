# Lakeflow Spark Declarative Pipelines (SDP)

**Major feature** · Available since ~2021 · DE Professional exam: S1

## What it is

SDP is the framework that used to be called Delta Live Tables. You declare datasets (streaming tables, materialized views, views) and the flows that feed them; the pipeline works out the dependency graph, orchestration, checkpoints, retries, scaling and table maintenance.

The Python module is `pyspark.pipelines`, imported as `dp`. The older `import dlt` still runs. The core was contributed to Apache Spark as Spark Declarative Pipelines; Lakeflow adds expectations, AUTO CDC, serverless and the event log on top.

## How it flows

1. **Source code**: Python or SQL files that declare tables and flows.
2. **Dataflow graph**: The pipeline resolves dependencies between datasets.
3. **Update**: Triggered (run and stop) or continuous. Each flow reads only new data where it can.
4. **Expectations**: Rows are checked; results are recorded.
5. **Published tables**: Streaming tables and materialized views in Unity Catalog, plus an event log.

```
[Source code] --> [Dataflow graph] --> [Update] --> [Expectations] --> [Published tables]
```

## When to choose it

**Choose it when**

- Medallion ETL where you want incremental processing without managing checkpoints.
- CDC and SCD targets.
- You need data quality rules with metrics recorded automatically.

**Pick something else when**

- Logic that needs arbitrary stateful operators, custom sinks per batch, or strict control of each micro-batch.
- Imperative steps such as calling an API and branching on the result: that is a job.

## Building blocks

| Object | Python | Use for |
|---|---|---|
| Streaming table | `@dp.table` or `dp.create_streaming_table` | Append-only incremental ingestion and CDC targets |
| Materialized view | `@dp.materialized_view` | Aggregations and joins that must always equal the query result |
| Temporary view | `@dp.temporary_view` | Intermediate logic that is not published |
| Flow | `@dp.append_flow`, `dp.create_auto_cdc_flow` | Writing into a target from one or more sources |
| Sink | `dp.create_sink` | Writing to Kafka, Event Hubs or an external Delta table |

## Senior engineer verdict

> I default to SDP for anything that looks like bronze, silver, gold. The value is not the syntax; it is that restarts, backfills, schema location, checkpoints and lineage are no longer my code. I drop to Structured Streaming only for the few flows that need what SDP does not expose.

## Examples

### 1. Bronze streaming table and silver with a quality rule

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_orders")
def bronze_orders():
    return (spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/Volumes/main/landing/orders/"))

@dp.table(name="silver_orders")
@dp.expect_or_drop("valid_id", "order_id IS NOT NULL")
def silver_orders():
    return (spark.readStream.table("bronze_orders")
        .withColumn("order_ts", F.to_timestamp("order_ts")))
```

### 2. Gold materialized view

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_daily_revenue")
def gold_daily_revenue():
    return (spark.read.table("silver_orders")
        .groupBy(F.to_date("order_ts").alias("order_date"))
        .agg(F.sum("amount").alias("revenue"), F.count("*").alias("orders")))
```

## Traps and gotchas

- Triggered pipelines stop after an update; continuous pipelines keep compute running.
- Development mode reuses compute and does not retry; production mode restarts and retries.
- Pipeline tables are owned by the pipeline. You do not write to them from outside.

## Sub-features

- [Streaming table or materialized view](streaming-table-vs-mv/README.md)
- [Expectations (data quality)](expectations/README.md)
- [AUTO CDC (formerly APPLY CHANGES)](auto-cdc/README.md)
- [AUTO CDC FROM SNAPSHOT](auto-cdc-from-snapshot/README.md)
- [Append flows and sinks](flows-and-sinks/README.md)
