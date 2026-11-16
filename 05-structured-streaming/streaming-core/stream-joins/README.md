# Stream-static and stream-stream joins

Available since ~2018 · DE Professional exam: S1 · Part of [Triggers, checkpoints and exactly-once](../README.md)

## What it is

A stream-static join looks up each micro-batch against the latest version of a Delta table and keeps no state. A stream-stream join buffers both sides in state and needs watermarks and a time-range condition so old rows can be evicted.

## How it flows

1. **Left stream row**: An ad impression.
2. **Buffered in state**: Waits for a matching click.
3. **Right stream row**: A click arrives within the allowed interval.
4. **Match emitted**: Joined row is output.
5. **Eviction**: Rows older than watermark plus interval are dropped; outer joins emit unmatched rows then.

```
[Left stream row] --> [Buffered in state] --> [Right stream row] --> [Match emitted] --> [Eviction]
```

## When to choose it

**Choose it when**

- Stream-static: enrich events with a dimension.
- Stream-stream: correlate two event streams within a time bound.

**Pick something else when**

- Stream-static when late dimension changes must correct past output: use a materialized view.

## Senior engineer verdict

> Stream-static is cheap and good enough for most enrichment, as long as everyone accepts that a row is joined with the dimension as it was when the row was processed.

## Examples

### 1. Stream-static enrichment

File: [`example_1.py`](example_1.py)

```python
orders = spark.readStream.table("main.silver.orders")
customers = spark.read.table("main.silver.customers")     # re-read each micro-batch
enriched = orders.join(customers, "customer_id", "left")
```

### 2. Stream-stream join with watermarks and a time bound

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F
imp = spark.readStream.table("main.silver.impressions").withWatermark("imp_ts", "2 hours").alias("imp")
clk = spark.readStream.table("main.silver.clicks").withWatermark("clk_ts", "3 hours").alias("clk")
joined = imp.join(clk, F.expr("""
    imp.ad_id = clk.ad_id AND
    clk_ts BETWEEN imp_ts AND imp_ts + INTERVAL 1 HOUR"""), "leftOuter")
```

## Traps and gotchas

- Outer stream-stream joins require watermarks and a time constraint.
- In a stream-static join, new rows in the static table do not trigger output; only the stream side does.
