# Triggers, backfills and cleanup

Available since ~2021 · DE Professional exam: S1, S5 · Part of [Auto Loader](../README.md)

## What it is

How you run Auto Loader decides its cost. `availableNow` processes everything pending in rate-limited micro-batches and then stops, which gives batch cost with streaming guarantees. A processing-time trigger keeps the stream running.

## How it flows

1. **Schedule fires**: A job starts the stream.
2. **availableNow**: All files discovered so far are processed in several micro-batches.
3. **Checkpoint commit**: Each batch commits offsets and file state.
4. **Stream stops**: Compute shuts down until the next run.

```
[Schedule fires] --> [availableNow] --> [Checkpoint commit] --> [Stream stops]
```

## When to choose it

**Choose it when**

- availableNow: hourly or daily freshness is fine.
- Processing-time or continuous pipeline: you need minutes or less.

**Pick something else when**

- `Trigger.Once`: deprecated and ignores rate limits.

## Senior engineer verdict

> Most 'streaming' pipelines I review should be availableNow on a schedule. You keep exactly-once and schema evolution and pay for minutes, not for an always-on cluster.

## Examples

### 1. Scheduled incremental run with file archiving

File: [`example_1.py`](example_1.py)

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/logs/_schema")
    .option("cloudFiles.cleanSource", "MOVE")
    .option("cloudFiles.cleanSource.moveDestination", "s3://acme-archive/logs/")
    .load("s3://acme-landing/logs/")
  .writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/logs")
    .trigger(availableNow=True).toTable("main.bronze.logs"))
```

### 2. Skip history, pick up only new files

File: [`example_2.py`](example_2.py)

```python
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.includeExistingFiles", "false")
    .option("cloudFiles.backfillInterval", "1 day")     # classic notification safety net
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/tx/_schema")
    .load("s3://acme-landing/tx/"))
```

## Traps and gotchas

- `includeExistingFiles` is read only on the first start of a stream.
- A file overwritten in place is not reprocessed unless `cloudFiles.allowOverwrites` is true.
