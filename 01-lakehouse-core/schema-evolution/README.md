# Schema enforcement and evolution

Available since ~2019 · DE Professional exam: S1, S2

## What it is

Delta rejects writes whose columns or types do not match the table. Evolution is opt-in: `mergeSchema` adds new columns on append, `overwriteSchema` replaces the schema on overwrite, and MERGE can evolve with `WITH SCHEMA EVOLUTION` or `withSchemaEvolution()`.

## How it flows

1. **Incoming DataFrame**: Has a new column `coupon`.
2. **Enforcement check**: Without an option the write fails with a schema mismatch.
3. **Evolution option**: `mergeSchema` tells Delta to add the column.
4. **New commit**: Metadata action records the new schema; old rows read the column as null.

```
[Incoming DataFrame] --> [Enforcement check] --> [Evolution option] --> [New commit]
```

## When to choose it

**Choose it when**

- Sources add columns over time and you want pipelines to keep running.
- You want bad writes to fail loudly by default.

**Pick something else when**

- Type changes that are not widening, such as string to int. Those need an explicit rewrite.

## Senior engineer verdict

> I enable evolution in bronze and silver ingestion and keep gold strict. A silently added column in a gold table is a contract change that someone should review.

## Examples

### 1. Add new columns on append

File: [`example_1.py`](example_1.py)

```python
(new_df.write.mode("append")
    .option("mergeSchema", "true")
    .saveAsTable("main.silver.orders"))
```

### 2. MERGE that evolves the target schema

File: [`example_2.py`](example_2.py)

```python
from delta.tables import DeltaTable
(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(updates.alias("s"), "t.customer_id = s.customer_id")
    .withSchemaEvolution()
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute())
```

## Traps and gotchas

- `mergeSchema` adds columns; it does not drop or rename them. Renames need column mapping.
- `overwriteSchema` only applies with mode overwrite.
