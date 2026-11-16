# SCD type 2 with MERGE

Available since ~2019 · DE Professional exam: S1 · Part of [SCD types and which one to choose](../README.md)

## What it is

Hand-written type 2 closes the current row and inserts a new one in the same MERGE. The usual trick stages each changed row twice: once with the real key so it matches and closes the old version, once with a null merge key so it falls through to the insert clause.

## How it flows

1. **Incoming changes**: Latest row per key.
2. **Find real changes**: Join to current rows and compare tracked columns.
3. **Stage twice**: Null merge key for the new version, real key for the close.
4. **MERGE**: Matched: set end date and current flag false. Not matched: insert the new current row.

```
[Incoming changes] --> [Find real changes] --> [Stage twice] --> [MERGE]
```

## When to choose it

**Choose it when**

- You are not in a pipeline, or you need extra columns and rules AUTO CDC does not offer.

**Pick something else when**

- Feeds with out-of-order events. This pattern assumes changes arrive in order.

## Senior engineer verdict

> I can write this from memory and I still prefer AUTO CDC, because this version quietly corrupts history when a late event arrives. If you must hand-write it, compare a hash of the tracked columns and make the job idempotent.

## Examples

### 1. Close old version and insert new one in a single MERGE

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
from delta.tables import DeltaTable
tgt = DeltaTable.forName(spark, "main.gold.dim_customer")
cur = tgt.toDF().where("is_current")

changed = (src.alias("s").join(cur.alias("t"), "customer_id")
    .where("s.address <> t.address OR s.segment <> t.segment").select("s.*"))

staged = (changed.withColumn("merge_key", F.lit(None).cast("string"))
    .unionByName(src.withColumn("merge_key", F.col("customer_id"))))

(tgt.alias("t").merge(staged.alias("s"), "t.customer_id = s.merge_key AND t.is_current")
    .whenMatchedUpdate(
        condition="t.address <> s.address OR t.segment <> s.segment",
        set={"is_current": "false", "end_date": "s.effective_date"})
    .whenNotMatchedInsert(values={
        "customer_id": "s.customer_id", "address": "s.address", "segment": "s.segment",
        "start_date": "s.effective_date", "end_date": "null", "is_current": "true"})
    .execute())
```

### 2. Change detection with a hash of tracked columns

File: [`example_2.py`](example_2.py)

```python
tracked = ["address", "segment", "tier"]
src_h = src.withColumn("row_hash", F.sha2(F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("")) for c in tracked]), 256))
changed = (src_h.alias("s").join(cur.alias("t"), "customer_id", "left")
    .where("t.customer_id IS NULL OR s.row_hash <> t.row_hash")
    .select("s.*"))
```

## Traps and gotchas

- Comparing columns with `<>` misses changes to or from NULL. Use a null-safe comparison or a hash with coalesce.
- Brand-new keys match nothing and are inserted by the not-matched clause through the real-key copy.
