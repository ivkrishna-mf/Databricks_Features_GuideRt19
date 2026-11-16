# transformWithState and real-time mode

Available since ~2025 · Part of [Triggers, checkpoints and exactly-once](../README.md)

## What it is

`transformWithState` is the current API for custom stateful streaming: per key you keep typed state (value, list, map), register timers and set time-to-live, which covers sessionization, alerting and state machines. Real-time mode runs supported queries with very low latency (milliseconds) for operational use cases such as fraud scoring, instead of micro-batches.

## How it flows

1. **Grouped stream**: Events keyed by user or device.
2. **StatefulProcessor**: init creates state; handleInputRows updates it.
3. **Timers and TTL**: Fire logic after inactivity; expire old state.
4. **Emit rows**: Your processor decides what to output.
5. **Real-time trigger**: Optional: process records as they arrive.

```
[Grouped stream] --> [StatefulProcessor] --> [Timers and TTL] --> [Emit rows] --> [Real-time trigger]
```

## When to choose it

**Choose it when**

- Business logic that built-in aggregations cannot express.
- Latency requirements below what micro-batches give.

**Pick something else when**

- Windowed counts and deduplication: built-in operators are simpler.
- Real-time mode for heavy aggregations into Delta: it targets low-latency pipelines with supported sinks such as Kafka.

## Senior engineer verdict

> Before writing a stateful processor I check whether a watermark plus a window or dropDuplicatesWithinWatermark does the job. When it does not, transformWithState with TTL is far safer than the older mapGroupsWithState, because state cannot grow without bound by accident.

## Examples

### 1. Running count per user with transformWithStateInPandas

File: [`example_1.py`](example_1.py)

```python
import pandas as pd
from pyspark.sql.streaming import StatefulProcessor, StatefulProcessorHandle
from pyspark.sql.types import StructType, StructField, LongType

class EventCounter(StatefulProcessor):
    def init(self, handle: StatefulProcessorHandle) -> None:
        self.count = handle.getValueState("count", StructType([StructField("n", LongType())]))

    def handleInputRows(self, key, rows, timerValues):
        n = self.count.get()[0] if self.count.exists() else 0
        for pdf in rows:
            n += len(pdf)
        self.count.update((n,))
        yield pd.DataFrame({"user_id": [key[0]], "events": [n]})

    def close(self) -> None:
        pass

counts = (spark.readStream.table("main.silver.events").groupBy("user_id")
    .transformWithStateInPandas(statefulProcessor=EventCounter(),
        outputStructType="user_id string, events long", outputMode="Update", timeMode="None"))
```

### 2. Real-time mode from Kafka to Kafka

File: [`example_2.py`](example_2.py)

```python
scored = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers).option("subscribe", "payments").load()
    .selectExpr("key", "CAST(value AS STRING) AS v")
    .selectExpr("key", "to_json(named_struct('v', v, 'risk', length(v) % 10)) AS value"))

(scored.writeStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers).option("topic", "payments-scored")
    .option("checkpointLocation", "/Volumes/main/ops/chk/payments_rt")
    .outputMode("update")
    .trigger(realTime="5 minutes")      # checkpoint interval; records flow continuously
    .start())
```

## Traps and gotchas

- transformWithState needs the RocksDB state store.
- Real-time mode supports a subset of sources, sinks and operators; check the docs for your runtime.
