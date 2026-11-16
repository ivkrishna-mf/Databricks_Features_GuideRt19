# foreachBatch

Available since ~2019 · DE Professional exam: S1 · Part of [Triggers, checkpoints and exactly-once](../README.md)

## What it is

`foreachBatch` hands each micro-batch to your function as a normal DataFrame together with a batch id. Inside you can use any batch API: MERGE, writes to several tables, JDBC, calls to services.

## How it flows

1. **Micro-batch**: A DataFrame with a batch id.
2. **Your function**: Deduplicate, then MERGE or write.
3. **Several writes**: Each should be idempotent on the batch id.
4. **Checkpoint commit**: If the function fails midway, the batch is retried.

```
[Micro-batch] --> [Your function] --> [Several writes] --> [Checkpoint commit]
```

## When to choose it

**Choose it when**

- Upserts from a stream.
- Writing one stream to more than one sink.
- Sinks with no streaming writer.

**Pick something else when**

- Plain appends to Delta: `toTable` is simpler and exactly-once.

## Senior engineer verdict

> foreachBatch is at-least-once. If a batch fails after the first of two writes, the retry repeats the first. I make each write idempotent with MERGE or with `txnAppId` and `txnVersion`, and I cache the batch only when I write it more than once.

## Examples

### 1. Idempotent writes to two tables

File: [`example_1.py`](example_1.py)

```python
def write_two(batch_df, batch_id):
    batch_df.persist()
    for table in ["main.silver.orders", "main.audit.orders_log"]:
        (batch_df.write.format("delta").mode("append")
            .option("txnAppId", "orders_" + table).option("txnVersion", batch_id)
            .saveAsTable(table))
    batch_df.unpersist()

(spark.readStream.table("main.bronze.orders").writeStream
    .foreachBatch(write_two)
    .option("checkpointLocation", "/Volumes/main/ops/chk/orders_two").start())
```

### 2. Streaming aggregation upserted with MERGE (update mode)

File: [`example_2.py`](example_2.py)

```python
from delta.tables import DeltaTable
def upsert_counts(batch_df, batch_id):
    (DeltaTable.forName(batch_df.sparkSession, "main.gold.user_counts").alias("t")
        .merge(batch_df.alias("s"), "t.user_id = s.user_id")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

(spark.readStream.table("main.silver.events").groupBy("user_id").count()
    .writeStream.outputMode("update").foreachBatch(upsert_counts)
    .option("checkpointLocation", "/Volumes/main/ops/chk/user_counts").start())
```

## Traps and gotchas

- Use `batch_df.sparkSession` inside the function, not a global session, on shared compute.
- The exactly-once guarantee of the Delta sink does not extend to custom code in foreachBatch.
