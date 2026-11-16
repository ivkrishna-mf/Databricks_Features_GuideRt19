# Kafka, Kinesis and Pub/Sub

Available since ~2016 · DE Professional exam: S2

## What it is

Structured Streaming reads message buses with offsets stored in the checkpoint. The payload arrives as binary `key` and `value` columns that you decode yourself.

## How it flows

1. **Producers**: Write events to a topic.
2. **Streaming source**: Reads from the offsets recorded in the checkpoint.
3. **Decode**: Cast value to string, then `from_json`, `from_avro` or `parse_json`.
4. **Bronze**: Append with topic, partition, offset and timestamp for replay.

```
[Producers] --> [Streaming source] --> [Decode] --> [Bronze]
```

## When to choose it

**Choose it when**

- Event data with latency needs of seconds to minutes.
- Decoupling producers from the lakehouse.

**Pick something else when**

- The retention of the topic is shorter than your worst outage. Land raw events in bronze first.

## Senior engineer verdict

> I always persist the raw bytes and Kafka metadata in bronze before parsing. Topics expire; a bronze table lets me fix a parsing bug and replay. Rate-limit with `maxOffsetsPerTrigger` so a backlog does not blow up one micro-batch.

## Examples

### 1. Kafka to bronze

File: [`example_1.py`](example_1.py)

```python
raw = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers)
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", 200000)
    .load())
(raw.selectExpr("CAST(key AS STRING) k", "CAST(value AS STRING) v",
                "topic", "partition", "offset", "timestamp")
    .writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/kafka_orders")
    .toTable("main.bronze.orders_events"))
```

### 2. Kinesis in a pipeline, parsed to VARIANT

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_clicks")
def bronze_clicks():
    return (spark.readStream.format("kinesis")
        .option("streamName", "clicks")
        .option("initialPosition", "TRIM_HORIZON")
        .load()
        .select(F.parse_json(F.col("data").cast("string")).alias("payload"),
                "approximateArrivalTimestamp"))
```

## Traps and gotchas

- `startingOffsets` is used only when the checkpoint is new.
- A pipeline full refresh re-reads the topic. If retention has passed, that data is gone.
