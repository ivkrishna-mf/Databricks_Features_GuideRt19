# Reading streaming state and checkpoint metadata

Available since ~2024 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

The state data source reads the state store of a streaming query straight from its checkpoint as a DataFrame, and the state metadata source lists the stateful operators and batches. This turns stateful streaming debugging from guesswork into a query.

## How it flows

1. **Checkpoint**: Written by a running or stopped query.
2. **state-metadata**: Lists operators, partitions and batch range.
3. **statestore**: Reads keys and values of an operator.
4. **Investigate**: Find oversized keys, stuck windows, missing deduplication entries.

```
[Checkpoint] --> [state-metadata] --> [statestore] --> [Investigate]
```

## When to choose it

**Choose it when**

- State is growing unexpectedly.
- Verifying what a deduplication or aggregation remembers.

**Pick something else when**

- Writing to a checkpoint by hand.

## Senior engineer verdict

> When a stateful job slows down, I read its state first. Nine times out of ten the watermark is not advancing for one partition, and the state store shows it immediately.

## Examples

### 1. List stateful operators in a checkpoint

File: [`example_1.py`](example_1.py)

```python
meta = spark.read.format("state-metadata").load("/Volumes/main/ops/chk/device_5m")
meta.select("operatorId", "operatorName", "stateStoreName", "numPartitions",
            "minBatchId", "maxBatchId").show(truncate=False)
```

### 2. Read state contents and find the biggest keys

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F
state = (spark.read.format("statestore")
    .option("operatorId", 0)
    .load("/Volumes/main/ops/chk/device_5m"))
state.select("key.*", "value.*", "partition_id").show(5, truncate=False)
state.groupBy("partition_id").count().orderBy(F.desc("count")).show(5)
```

## Traps and gotchas

- The reader works on the checkpoint path, not on the target table.
