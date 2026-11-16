# SCD types 3, 4 and 6

Available since ~2019 · DE Professional exam: S9 · Part of [SCD types and which one to choose](../README.md)

## What it is

Type 3 keeps a previous-value column. Type 4 moves history to a separate table. Type 6 is a type 2 table that also carries the current value on every row, so one join answers both as-was and as-is questions.

## How it flows

1. **Change arrives**: Region changes from North to West.
2. **Type 3**: previous_region = North, region = West.
3. **Type 4**: Current table updated; old row appended to the history table.
4. **Type 6**: New version row added and current_region updated on all rows of the key.

```
[Change arrives] --> [Type 3] --> [Type 4] --> [Type 6]
```

## When to choose it

**Choose it when**

- Type 3: a one-off reorganization where reports compare old and new.
- Type 4: attributes that change often and would bloat the dimension.
- Type 6: BI tools that cannot do range joins.

**Pick something else when**

- Type 3 when more than one prior value will ever be needed.

## Senior engineer verdict

> Type 6 looks attractive and costs a rewrite of every version on each change. I usually give BI a type 2 table plus a current view and get the same result with no extra writes.

## Examples

### 1. Type 3: shift the current value into a previous column

File: [`example_1.py`](example_1.py)

```python
from delta.tables import DeltaTable
(DeltaTable.forName(spark, "main.gold.dim_store").alias("t")
    .merge(updates.alias("s"), "t.store_id = s.store_id")
    .whenMatchedUpdate(condition="t.region <> s.region",
        set={"previous_region": "t.region", "region": "s.region", "region_changed_on": "s.effective_date"})
    .whenNotMatchedInsert(values={"store_id": "s.store_id", "region": "s.region",
        "previous_region": "null", "region_changed_on": "s.effective_date"})
    .execute())
```

### 2. Type 4: current table and a history table from one feed

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import col
for name, scd in [("customer_current", 1), ("customer_history", 2)]:
    dp.create_streaming_table(name)
    dp.create_auto_cdc_flow(target=name, source="customers_cdc", keys=["customer_id"],
        sequence_by=col("commit_ts"), stored_as_scd_type=scd, name=name + "_flow")
```

## Traps and gotchas

- Type 3 adds columns, type 2 adds rows.
