# File detection modes

Available since ~2020 · DE Professional exam: S2 · Part of [Auto Loader](../README.md)

## What it is

Auto Loader finds new files in one of three ways. Directory listing lists the input path. Classic file notification creates a queue and subscription per stream. File events uses one managed queue per Unity Catalog external location and is the current recommendation.

## How it flows

1. **File created**: Object storage records the new object.
2. **Storage event**: With file events enabled, the event goes to a queue managed for the external location.
3. **File events cache**: Databricks keeps recent file metadata for all streams on that location.
4. **Auto Loader reads cache**: The stream asks for files after its stored position. No listing.
5. **Periodic full listing**: Databricks lists the location on a schedule to catch anything missed.

```
[File created] --> [Storage event] --> [File events cache] --> [Auto Loader reads cache] --> [Periodic full listing]
```

## Choosing a mode

| Mode | How to enable | Choose when | Watch out |
|---|---|---|---|
| Directory listing (default) | Nothing | Small directories, quick start, no cloud permissions for queues | Listing cost and latency grow with file count; incremental listing is deprecated |
| File notification, classic | `cloudFiles.useNotifications` = true | Legacy setups, or very low latency directly from the queue | One queue per stream; cloud limits on notifications per bucket; needs elevated cloud permissions |
| File notification with file events | Enable file events on the external location, then `cloudFiles.useManagedFileEvents` = true | Most workloads on Unity Catalog; many streams on one bucket | Runtime 14.3 LTS or above; run the stream at least once every 7 days or it falls back to a full listing |

## Senior engineer verdict

> On Unity Catalog I enable file events on the external location once and every stream benefits. I keep directory listing only for small landing folders where a queue is not worth a conversation with the cloud team. You can switch modes between restarts and keep exactly-once.

## Examples

### 1. File events mode

File: [`example_1.py`](example_1.py)

```python
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.useManagedFileEvents", "true")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/iot/_schema")
    .load("s3://acme-landing/iot/"))       # path under a UC external location
```

### 2. Classic notification mode with rate limits

File: [`example_2.py`](example_2.py)

```python
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.useNotifications", "true")
    .option("cloudFiles.maxFilesPerTrigger", 500)
    .option("cloudFiles.maxBytesPerTrigger", "10g")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/clicks/_schema")
    .load("abfss://landing@acme.dfs.core.windows.net/clicks/"))
```

## Traps and gotchas

- Changing the input path is supported in directory listing mode, not in file notification mode.
- 'Millions of files and listing is slow or expensive' points to file notifications with file events.
- Neither mode guarantees ordering.
