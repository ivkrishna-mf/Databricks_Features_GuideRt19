# Deletion vectors

Available since ~2023 · DE Professional exam: S5, S6

## What it is

Without deletion vectors, deleting one row rewrites the whole Parquet file. With them, Delta writes a small bitmap that marks rows as removed and readers skip those rows. DELETE, UPDATE and MERGE become much faster; the physical rewrite happens later during OPTIMIZE or REORG.

## How it flows

1. **DELETE one row**: In a large file.
2. **Write deletion vector**: A bitmap marks the row; the data file is untouched.
3. **Readers**: Apply the bitmap and skip the row.
4. **OPTIMIZE or REORG PURGE**: Rewrites the file without the row.
5. **VACUUM**: Removes the old file after retention.

```
[DELETE one row] --> [Write deletion vector] --> [Readers] --> [OPTIMIZE or REORG PURGE] --> [VACUUM]
```

## When to choose it

**Choose it when**

- Tables with frequent small updates, deletes or merges.
- Almost always: it is the default for new tables in most workspaces.

**Pick something else when**

- Old external readers that do not support the table feature.

## Senior engineer verdict

> Deletion vectors make writes cheap by deferring work, so the row is logically gone but still physically in the file. For privacy deletes that matters: the job is not finished until REORG PURGE and VACUUM have run.

## Examples

### 1. Enable and delete

File: [`example_1.py`](example_1.py)

```python
spark.sql("ALTER TABLE main.silver.customers SET TBLPROPERTIES ('delta.enableDeletionVectors' = true)")
spark.sql("DELETE FROM main.silver.customers WHERE customer_id = 'C-1042'")
spark.sql("DESCRIBE HISTORY main.silver.customers").select("operation", "operationMetrics").show(1, False)
```

### 2. Physically remove soft-deleted rows

File: [`example_2.py`](example_2.py)

```python
spark.sql("REORG TABLE main.silver.customers APPLY (PURGE)")      # rewrite files that have deletion vectors
spark.sql("VACUUM main.silver.customers RETAIN 168 HOURS")       # then drop old files after 7 days
```

## Traps and gotchas

- Enabling deletion vectors upgrades the table protocol; older clients cannot read it.
- A deleted row remains in the data file until it is rewritten and vacuumed.
