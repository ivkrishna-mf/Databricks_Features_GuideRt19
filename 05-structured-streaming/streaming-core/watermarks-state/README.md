# Watermarks, state and output modes

**Major feature** · Available since ~2017 · DE Professional exam: S1 · Part of [Triggers, checkpoints and exactly-once](../README.md)

## What it is

Stateful operators (windowed aggregations, deduplication, stream-stream joins) keep data in a state store between batches. A watermark tells the engine how late data may arrive: watermark = max event time seen minus the threshold. State older than the watermark is dropped, and rows older than it are discarded.

## How it flows

1. **Event arrives**: With an event-time column.
2. **Update max event time**: Tracked across the stream.
3. **Compute watermark**: Max event time minus the delay, for example 10 minutes.
4. **Aggregate in state**: The matching window is updated.
5. **Emit and evict**: In append mode a window is emitted once the watermark passes its end; its state is then removed.

```
[Event arrives] --> [Update max event time] --> [Compute watermark] --> [Aggregate in state] --> [Emit and evict]
```

## When to choose it

**Choose it when**

- Any aggregation, deduplication or join on an unbounded stream.

**Pick something else when**

- Unbounded state: aggregation or dropDuplicates without a watermark grows until the job fails.

## Output modes

| Mode | Emits | Works with |
|---|---|---|
| append (default) | Only rows that will never change again | Stateless queries; aggregations only with a watermark |
| update | Rows changed in this batch | Aggregations; use `foreachBatch` with MERGE to write to Delta |
| complete | The whole result every batch | Small aggregations without watermark eviction |

## Senior engineer verdict

> The watermark delay is a business decision: how long are we willing to wait for late data before publishing a number. Longer delay means more complete results, more state and later output. I size it from measured lateness, not from a guess, and use RocksDB as the state store once state is more than a few million keys.

## Examples

### 1. Tumbling window aggregation with late data bound

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
agg = (spark.readStream.table("main.silver.events")
    .withWatermark("event_ts", "10 minutes")
    .groupBy(F.window("event_ts", "5 minutes"), "device_id")
    .agg(F.count("*").alias("events"), F.avg("temp").alias("avg_temp")))
(agg.writeStream.outputMode("append")
    .option("checkpointLocation", "/Volumes/main/ops/chk/device_5m")
    .toTable("main.gold.device_5m"))
```

### 2. Streaming deduplication with bounded state

File: [`example_2.py`](example_2.py)

```python
spark.conf.set("spark.sql.streaming.stateStore.providerClass",
    "com.databricks.sql.streaming.state.RocksDBStateStoreProvider")
dedup = (spark.readStream.table("main.bronze.payments")
    .withWatermark("paid_at", "1 hour")
    .dropDuplicatesWithinWatermark(["payment_id"]))
```

## Traps and gotchas

- In append mode, a window appears in the output only after the watermark passes the window end. 'No rows yet' is often correct behavior.
- `dropDuplicates` with a watermark only bounds state if the event-time column is in the key list; `dropDuplicatesWithinWatermark` removes that requirement.
- Data later than the watermark is dropped silently.
