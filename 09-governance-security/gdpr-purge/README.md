# Data purging and right to erasure

**Major feature** · Available since ~2023 · DE Professional exam: S6

## What it is

Deleting a row in Delta removes it from the current version only. Earlier versions, deletion vectors, change feed files and downstream copies still hold it until they are rewritten and vacuumed. A compliant purge covers all of them within the deadline.

## How it flows

1. **Erasure request**: Added to a control table of keys to delete.
2. **DELETE in every layer**: Bronze, silver and gold, driven by the control table.
3. **REORG PURGE**: Rewrites files that only hide rows behind deletion vectors.
4. **VACUUM**: After retention, removes old files so time travel cannot return the rows.
5. **Verify and log**: Record completion for audit.

```
[Erasure request] --> [DELETE in every layer] --> [REORG PURGE] --> [VACUUM] --> [Verify and log]
```

## When to choose it

**Choose it when**

- Any table holding personal data.

**Pick something else when**

- Long retention settings on tables with personal data: they extend how long deleted rows physically exist.

## Senior engineer verdict

> I design for deletion on day one: a consistent subject key in every table, short retention on PII tables, and a scheduled purge job that reads requests, deletes, purges and vacuums. Streams that read tables receiving deletes use `skipChangeCommits` or the change feed so the delete does not break them. Where the platform offers automatic row expiry (auto TTL), I use it for retention-based deletion.

## Examples

### 1. Delete across tables from a request list

File: [`example_1.py`](example_1.py)

```python
keys = spark.table("main.privacy.erasure_requests").where("status = 'OPEN'").select("customer_id")
keys.createOrReplaceTempView("to_erase")
for t in ["main.bronze.customers", "main.silver.customers", "main.silver.orders"]:
    spark.sql(f"DELETE FROM {t} WHERE customer_id IN (SELECT customer_id FROM to_erase)")
```

### 2. Make the deletion physical

File: [`example_2.py`](example_2.py)

```python
for t in ["main.bronze.customers", "main.silver.customers", "main.silver.orders"]:
    spark.sql(f"ALTER TABLE {t} SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 7 days')")
    spark.sql(f"REORG TABLE {t} APPLY (PURGE)")
    spark.sql(f"VACUUM {t}")                 # removes files older than the retention
```

## Traps and gotchas

- After DELETE the data is still reachable by time travel until VACUUM removes the files.
- With deletion vectors, run REORG PURGE before VACUUM or the row stays in the Parquet file.
- Materialized views and streaming tables downstream must also be refreshed or cleaned.
