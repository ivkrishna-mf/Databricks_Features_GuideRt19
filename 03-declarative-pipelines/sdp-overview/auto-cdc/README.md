# AUTO CDC (formerly APPLY CHANGES)

**Major feature** · Available since ~2021 · DE Professional exam: S1, S2 · Part of [Lakeflow Spark Declarative Pipelines (SDP)](../README.md)

## What it is

AUTO CDC applies a change feed (inserts, updates, deletes with a sequence column) to a target streaming table as SCD type 1 or type 2. It orders events by `sequence_by`, so late and out-of-order changes are applied correctly, which is the hard part of hand-written MERGE.

## How it flows

1. **CDC feed**: Rows with a key, an operation and a sequence value.
2. **create_auto_cdc_flow**: Declares keys, sequence, delete condition and SCD type.
3. **Ordering**: Events are applied by sequence, not by arrival.
4. **SCD1 target**: One current row per key.
5. **SCD2 target**: A row per version with `__START_AT` and `__END_AT`.

```
[CDC feed] --> [create_auto_cdc_flow] --> [Ordering] --> [SCD1 target] --> [SCD2 target]
```

## When to choose it

**Choose it when**

- Any CDC feed inside a pipeline: Debezium, a database change table, a Delta change feed.
- You need SCD2 without writing merge logic.

**Pick something else when**

- Only full snapshots exist: use AUTO CDC FROM SNAPSHOT.
- Outside a pipeline: use MERGE in foreachBatch.

## Senior engineer verdict

> The parameter that decides correctness is `sequence_by`. It must increase with the true order of changes at the source: a log sequence number or commit timestamp, never the ingestion time. For ties I pass a struct of two columns. For SCD2 I list only the columns whose history the business cares about, otherwise every noisy column creates a new version.

## Examples

### 1. SCD type 1: keep the latest row

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.temporary_view
def customers_cdc():
    return spark.readStream.table("main.bronze.customers_cdc")

dp.create_streaming_table("silver_customers")
dp.create_auto_cdc_flow(
    target="silver_customers",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by=col("commit_ts"),
    apply_as_deletes=expr("op = 'DELETE'"),
    except_column_list=["op", "commit_ts"],
    stored_as_scd_type=1)
```

### 2. SCD type 2: history for selected columns

File: [`example_2.py`](example_2.py)

```python
dp.create_streaming_table("dim_customer_history")
dp.create_auto_cdc_flow(
    target="dim_customer_history",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by=col("commit_ts"),
    apply_as_deletes=expr("op = 'DELETE'"),
    except_column_list=["op", "commit_ts"],
    stored_as_scd_type=2,
    track_history_column_list=["address", "segment"])
# Current rows: WHERE __END_AT IS NULL
```

### 3. Same flow in SQL

File: [`example_3.sql`](example_3.sql)

```sql
CREATE OR REFRESH STREAMING TABLE dim_customer_history;

CREATE FLOW customer_cdc AS AUTO CDC INTO dim_customer_history
FROM stream(main.bronze.customers_cdc)
KEYS (customer_id)
APPLY AS DELETE WHEN op = 'DELETE'
SEQUENCE BY commit_ts
COLUMNS * EXCEPT (op, commit_ts)
STORED AS SCD TYPE 2;
```

## Traps and gotchas

- AUTO CDC needs Pro or Advanced edition, or serverless. It is a Lakeflow feature, not part of open-source Spark Declarative Pipelines.
- Default is SCD type 1.
- `apply_as_truncates` works with SCD type 1 only.
- The target of AUTO CDC has updates and deletes. A downstream stream must read its change feed or use `skipChangeCommits`.
