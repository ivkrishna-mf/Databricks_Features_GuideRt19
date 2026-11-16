# Append flows and sinks

Available since ~2024 · DE Professional exam: S1 · Part of [Lakeflow Spark Declarative Pipelines (SDP)](../README.md)

## What it is

A flow is a query that writes into a target. Several append flows can feed one streaming table, which lets you union sources or add a new source later without a full refresh. A sink lets a pipeline write to Kafka, Event Hubs or an external Delta table.

## How it flows

1. **Two sources**: For example two regional topics.
2. **One append flow each**: Each has its own checkpoint.
3. **Shared target**: A single streaming table.
4. **Optional sink**: Another flow publishes curated events to Kafka.

```
[Two sources] --> [One append flow each] --> [Shared target] --> [Optional sink]
```

## When to choose it

**Choose it when**

- Merging several streams into one table.
- One-time backfill into an existing streaming table with `once=True`.
- Reverse ETL of events to a bus.

**Pick something else when**

- Using `union` inside one query: adding a source later then forces a full refresh.

## Senior engineer verdict

> Append flows are how I add a source to a live table safely. Each flow owns its checkpoint, so the existing ones keep their position.

## Examples

### 1. Two flows into one streaming table

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
dp.create_streaming_table("bronze_orders_all")

@dp.append_flow(target="bronze_orders_all", name="orders_eu")
def orders_eu():
    return spark.readStream.table("main.bronze.orders_eu")

@dp.append_flow(target="bronze_orders_all", name="orders_us")
def orders_us():
    return spark.readStream.table("main.bronze.orders_us")
```

### 2. Publish to Kafka through a sink

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

dp.create_sink(name="alerts_kafka", format="kafka",
    options={"kafka.bootstrap.servers": brokers, "topic": "fraud-alerts"})

@dp.append_flow(target="alerts_kafka", name="fraud_to_kafka")
def fraud_to_kafka():
    return (spark.readStream.table("silver_fraud_scores").where("score > 0.9")
        .select(F.col("txn_id").alias("key"), F.to_json(F.struct("*")).alias("value")))
```

## Traps and gotchas

- Sinks accept append flows only.
- Renaming a flow creates a new checkpoint, which reprocesses from the start.
