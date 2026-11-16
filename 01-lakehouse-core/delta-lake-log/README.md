# Delta Lake transaction log

**Major feature** · Available since ~2017 · DE Professional exam: S5, S9

## What it is

A Delta table is Parquet files plus a `_delta_log` folder of ordered JSON commits. Each commit lists files added and removed, so readers see a consistent snapshot and writers get ACID transactions through optimistic concurrency.

Because old files stay until VACUUM removes them, you can query earlier versions (time travel) and roll back with RESTORE.

## How it flows

1. **Writer stages files**: New Parquet files are written. Nothing is visible yet.
2. **Commit N.json**: The writer tries to create the next numbered commit. If another writer got there first, Delta checks for a real conflict and retries.
3. **Checkpoint**: Periodically the log state is compacted into a Parquet checkpoint so readers do not replay every commit.
4. **Reader snapshot**: A reader loads the latest checkpoint plus later commits and reads only the files in that snapshot.
5. **Time travel and VACUUM**: Old versions stay queryable until log and file retention expire and VACUUM deletes unreferenced files.

```
[Writer stages files] --> [Commit N.json] --> [Checkpoint] --> [Reader snapshot] --> [Time travel and VACUUM]
```

## When to choose it

**Choose it when**

- Always. Every table in Unity Catalog should be Delta, or Iceberg where an external engine requires it.
- You need concurrent writers, upserts, deletes, or an audit trail of changes.

**Pick something else when**

- You plan to keep years of history through time travel. Retention defaults are 30 days of log and 7 days of removed files; use an SCD2 table for long history.

## Senior engineer verdict

> I treat time travel as an operational undo, not as a history store. The two properties people confuse are `delta.logRetentionDuration` (how far back versions are listed) and `delta.deletedFileRetentionDuration` (how long the data files survive). You need both to travel back.

## Examples

### 1. History, time travel and restore

File: [`example_1.py`](example_1.py)

```python
df.write.mode("append").saveAsTable("main.sales.orders")

(spark.sql("DESCRIBE HISTORY main.sales.orders")
    .select("version", "timestamp", "operation", "operationMetrics")
    .show(5, truncate=False))

before = spark.read.option("versionAsOf", 12).table("main.sales.orders")
spark.sql("RESTORE TABLE main.sales.orders TO VERSION AS OF 12")
```

### 2. Idempotent append that survives a retry

File: [`example_2.py`](example_2.py)

```python
# Same (txnAppId, txnVersion) is written once, even if the task reruns
(df.write.format("delta").mode("append")
    .option("txnAppId", "orders_loader")
    .option("txnVersion", run_number)       # monotonically increasing per app
    .saveAsTable("main.sales.orders"))
```

## Traps and gotchas

- RESTORE fails if VACUUM already removed the files of the target version.
- Default isolation is WriteSerializable. Two appends never conflict; two MERGE or UPDATE statements touching the same files can.
- Time travel beyond the retention window is not guaranteed even if the version still shows in history.
