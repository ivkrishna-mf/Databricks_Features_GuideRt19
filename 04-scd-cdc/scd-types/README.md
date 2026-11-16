# SCD types and which one to choose

**Major feature** · Available since ~2019 · DE Professional exam: S1, S9

## What it is

A slowly changing dimension strategy answers one question: when an attribute changes, what happens to the old value? The answer drives storage, query complexity and what the business can ask later.

## How it flows

1. **Attribute changes**: A customer moves city.
2. **Does anyone need the old value?**: No: type 1.
3. **For point-in-time facts?**: Yes: type 2.
4. **Only the previous value?**: Type 3.
5. **Changes very frequently?**: Split into a history or mini-dimension: type 4.

```
[Attribute changes] --> [Does anyone need the old value?] --> [For point-in-time facts?] --> [Only the previous value?] --> [Changes very frequently?]
```

## Types

| Type | What it does | Choose when | Cost |
|---|---|---|---|
| 0 | Never update | Immutable attributes such as birth date or original signup channel | None |
| 1 | Overwrite in place | Corrections, or history has no business value | History is gone |
| 2 | New row per version with validity range and current flag | Facts must join to the value that was true at the time; audit | Table grows; joins need a range condition |
| 3 | Extra column for the previous value | Only one prior state matters, such as previous region after a reorg | No deeper history |
| 4 | Current table plus separate history table | Fast-changing attributes; most queries want current only | Two tables to maintain |
| 6 | Type 2 rows that also carry the current value (1 + 2 + 3) | Reports need both as-was and as-is without two joins | Updates touch all versions of a key |

## Senior engineer verdict

> Type 1 unless someone can name the report that needs history; type 2 for the dimensions that finance, compliance or attribution depend on. On Databricks I build type 1 and type 2 with AUTO CDC and reserve hand-written MERGE for types 3 and 6. And I never rely on Delta time travel for history: it is bounded by retention.

## Examples

### 1. Point-in-time join of a fact to an SCD2 dimension

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
f = spark.table("main.gold.fact_orders").alias("f")
d = spark.table("main.gold.dim_customer_history").alias("d")
as_was = f.join(d,
    (F.col("f.customer_id") == F.col("d.customer_id")) &
    (F.col("f.order_ts") >= F.col("d.__START_AT")) &
    (F.col("d.__END_AT").isNull() | (F.col("f.order_ts") < F.col("d.__END_AT"))))
```

### 2. Current view over the same dimension (as-is reporting)

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
CREATE OR REPLACE VIEW main.gold.dim_customer_current AS
SELECT * EXCEPT (__START_AT, __END_AT)
FROM main.gold.dim_customer_history
WHERE __END_AT IS NULL""")
```

## Traps and gotchas

- SCD2 rows from AUTO CDC use `__START_AT` and `__END_AT`; a null end means current.
- Time travel is not SCD2.

## Sub-features

- [SCD type 1 with MERGE](scd1-merge/README.md)
- [SCD type 2 with MERGE](scd2-merge/README.md)
- [SCD types 3, 4 and 6](scd3-4-6/README.md)
