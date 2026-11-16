# Triggers, checkpoints and exactly-once

**Major feature** · Available since ~2017 · DE Professional exam: S1

## What it is

A streaming query is a DataFrame query that runs repeatedly over new data. The checkpoint records which input offsets each micro-batch covered and the state of stateful operators. Exactly-once output needs three things: a replayable source, a checkpoint, and an idempotent sink such as Delta.

## How it flows

1. **Plan batch**: Write the offset range to the checkpoint before processing.
2. **Process**: Run the query over that range.
3. **Write to sink**: Delta commits with the query id and batch id.
4. **Commit**: Mark the batch done in the checkpoint.
5. **On failure**: Restart replays the same offsets; Delta skips a batch it already committed.

```
[Plan batch] --> [Process] --> [Write to sink] --> [Commit] --> [On failure]
```

## When to choose it

**Choose it when**

- Any incremental processing, including what people call batch.

**Pick something else when**

- Sharing one checkpoint between two queries. One query, one checkpoint.

## Triggers

| Trigger | Behavior | Choose when |
|---|---|---|
| Default (none) | Next micro-batch starts as soon as the previous one ends | Lowest latency with micro-batches |
| `processingTime="1 minute"` | Fixed interval | Predictable load, fewer small files |
| `availableNow=True` | Process the backlog in several batches and stop | Scheduled incremental batch |
| Real-time mode | Very low latency processing on supported sources and sinks | Operational use cases under a second |
| `once=True` | Single batch, deprecated | Do not choose |

## Senior engineer verdict

> The checkpoint is part of the application. I store it in a volume next to nothing else, name it after the target table, and treat 'delete the checkpoint' as a data migration, because it resets offsets and state.

## Examples

### 1. Scheduled incremental batch

File: [`example_1.py`](example_1.py)

```python
(spark.readStream.table("main.bronze.orders")
    .where("status IS NOT NULL")
    .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/silver_orders")
    .trigger(availableNow=True)
    .toTable("main.silver.orders"))
```

### 2. Read a Delta table that also receives updates

File: [`example_2.py`](example_2.py)

```python
stream = (spark.readStream
    .option("skipChangeCommits", "true")       # ignore commits that rewrite existing rows
    .option("maxFilesPerTrigger", 200)
    .table("main.silver.customers"))
```

## Traps and gotchas

- After changing aggregation keys, the stateful operator or the source, the old checkpoint is not reusable. Changing a filter or adding a projection is fine.
- A Delta source fails on non-append commits unless you set `skipChangeCommits` or read the change feed.
- `availableNow` honors rate limits; `once` does not.

## Sub-features

- [Watermarks, state and output modes](watermarks-state/README.md)
- [Stream-static and stream-stream joins](stream-joins/README.md)
- [foreachBatch](foreach-batch/README.md)
- [transformWithState and real-time mode](advanced-streaming/README.md)
