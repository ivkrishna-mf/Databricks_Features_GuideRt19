# SCD type 1 with MERGE

Available since ~2019 · DE Professional exam: S1 · Part of [SCD types and which one to choose](../README.md)

## What it is

Outside pipelines, type 1 is an upsert: update the row when the key matches and the incoming version is newer, insert it otherwise, delete on a delete marker.

## How it flows

1. **Change batch**: May hold several changes per key.
2. **Keep the latest per key**: Window by key, order by sequence descending.
3. **MERGE**: Match on key.
4. **Update, insert or delete**: One current row per key remains.

```
[Change batch] --> [Keep the latest per key] --> [MERGE] --> [Update, insert or delete]
```

## When to choose it

**Choose it when**

- Batch jobs or `foreachBatch` streams that are not in a pipeline.

**Pick something else when**

- Inside a pipeline: AUTO CDC with `stored_as_scd_type=1`.

## Senior engineer verdict

> The condition `s.seq > t.seq` on the update clause is what makes a rerun or a late batch harmless.

## Examples

### 1. Batch upsert with deletes

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F, Window
from delta.tables import DeltaTable
w = Window.partitionBy("customer_id").orderBy(F.col("seq").desc())
latest = changes.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(latest.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedDelete(condition="s.op = 'D'")
    .whenMatchedUpdateAll(condition="s.seq > t.seq")
    .whenNotMatchedInsertAll(condition="s.op <> 'D'")
    .execute())
```

### 2. The same upsert from a stream

File: [`example_2.py`](example_2.py)

```python
def upsert(batch_df, batch_id):
    w = Window.partitionBy("customer_id").orderBy(F.col("seq").desc())
    latest = batch_df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
    (DeltaTable.forName(batch_df.sparkSession, "main.silver.customers").alias("t")
        .merge(latest.alias("s"), "t.customer_id = s.customer_id")
        .whenMatchedUpdateAll(condition="s.seq > t.seq")
        .whenNotMatchedInsertAll().execute())

(spark.readStream.table("main.bronze.customers_cdc").writeStream
    .foreachBatch(upsert)
    .option("checkpointLocation", "/Volumes/main/ops/chk/customers_scd1")
    .trigger(availableNow=True).start())
```

## Traps and gotchas

- Clause order matters: the first matching WHEN MATCHED clause wins.
