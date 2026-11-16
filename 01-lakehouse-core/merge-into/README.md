# MERGE INTO

Available since ~2019 · DE Professional exam: S1, S3

## What it is

One atomic statement that inserts, updates and deletes target rows based on a join with a source. It is the base for upserts, deduplicated loads and hand-written SCD logic.

## How it flows

1. **Source batch**: New and changed rows, deduplicated to one row per key.
2. **Join on keys**: Delta finds target files that may hold matching keys.
3. **Apply clauses**: WHEN MATCHED update or delete, WHEN NOT MATCHED insert, WHEN NOT MATCHED BY SOURCE for rows missing from the source.
4. **Rewrite or mark**: Touched files are rewritten, or rows are marked with deletion vectors.
5. **Single commit**: Readers see all changes at once.

```
[Source batch] --> [Join on keys] --> [Apply clauses] --> [Rewrite or mark] --> [Single commit]
```

## When to choose it

**Choose it when**

- Batch or foreachBatch upserts outside a declarative pipeline.
- You need custom match logic that AUTO CDC cannot express.

**Pick something else when**

- Inside Lakeflow pipelines for CDC feeds: use AUTO CDC, which handles ordering and late events.

## Senior engineer verdict

> Nine out of ten MERGE incidents are duplicate keys in the source. I deduplicate with a window on the sequencing column before every MERGE, and I add a selective predicate on the target (a date range or clustering key) so Delta does not scan the whole table.

## Examples

### 1. Upsert with a deduplicated source

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F, Window
from delta.tables import DeltaTable
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())
latest = updates.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(latest.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedUpdateAll(condition="s.updated_at > t.updated_at")
    .whenNotMatchedInsertAll()
    .execute())
```

### 2. Delete target rows that left the source

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
MERGE INTO main.silver.products t
USING main.staging.products_snapshot s ON t.sku = s.sku
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE""")
```

## Traps and gotchas

- Multiple source rows matching one target row makes MERGE fail. Deduplicate first.
- A table changed by MERGE is no longer append-only, so a stream reading it needs `skipChangeCommits` or the change feed.
