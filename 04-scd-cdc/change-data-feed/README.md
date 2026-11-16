# Change Data Feed

**Major feature** · Available since ~2021 · DE Professional exam: S5

## What it is

Change Data Feed exposes the row-level changes between versions of a Delta table: inserts, deletes, and the before and after image of updates. Downstream jobs read only what changed, which avoids full recomputation.

On Runtime 19 with row tracking, changes are computed at query time (automatic change data feed), so you do not have to enable the feed on every table.

## How it flows

1. **Table is modified**: MERGE, UPDATE, DELETE or append.
2. **Changes recorded**: Per commit, with `_change_type`, `_commit_version`, `_commit_timestamp`.
3. **Consumer reads the feed**: Batch between versions, or as a stream.
4. **Apply downstream**: Update aggregates, propagate deletes, feed AUTO CDC.

```
[Table is modified] --> [Changes recorded] --> [Consumer reads the feed] --> [Apply downstream]
```

## When to choose it

**Choose it when**

- Silver tables with updates and deletes that feed gold incrementally.
- Propagating GDPR deletes downstream.
- Replicating a table to another system.

**Pick something else when**

- Append-only tables: a normal stream already gives you new rows.
- Keeping an audit trail forever: the feed follows table retention.

## Senior engineer verdict

> CDF is the bridge between a table that gets merged into and a stream that expects appends. The pattern I use most: AUTO CDC builds silver, silver's change feed drives gold. I filter out `update_preimage` unless I am maintaining an aggregate that needs to subtract the old value.

## Examples

### 1. Enable and read changes in batch

File: [`example_1.py`](example_1.py)

```python
spark.sql("ALTER TABLE main.silver.customers SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

changes = (spark.read
    .option("readChangeFeed", "true")
    .option("startingVersion", 15).option("endingVersion", 20)
    .table("main.silver.customers"))
changes.where("_change_type IN ('insert', 'update_postimage', 'delete')").show()
```

### 2. Stream the feed into a downstream MERGE

File: [`example_2.py`](example_2.py)

```python
from delta.tables import DeltaTable
def apply(batch, _):
    latest = batch.where("_change_type <> 'update_preimage'")   # dedupe per key in real code
    (DeltaTable.forName(batch.sparkSession, "main.gold.customer_360").alias("t")
        .merge(latest.alias("s"), "t.customer_id = s.customer_id")
        .whenMatchedDelete(condition="s._change_type = 'delete'")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

(spark.readStream.option("readChangeFeed", "true").table("main.silver.customers")
    .writeStream.foreachBatch(apply)
    .option("checkpointLocation", "/Volumes/main/ops/chk/customer_360").start())
```

## Traps and gotchas

- Four change types: insert, update_preimage, update_postimage, delete.
- Changes made before the feed was enabled are not available (classic CDF).
- VACUUM removes the files the feed needs for old versions.
