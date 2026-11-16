# Deep and shallow clone

Available since ~2020 · DE Professional exam: S8

## What it is

A deep clone copies data and metadata into an independent table. A shallow clone copies only metadata and points at the source files, so it is instant and cheap.

## How it flows

1. **Source table**: At a chosen version.
2. **CLONE**: Shallow copies the log; deep also copies data files incrementally.
3. **Independent log**: Writes to the clone never touch the source.
4. **Use**: Test a risky change, or keep a backup or archive copy.

```
[Source table] --> [CLONE] --> [Independent log] --> [Use]
```

## When to choose it

**Choose it when**

- Shallow: test a migration or a MERGE against production-shaped data.
- Deep: backup, archive, or move a table between catalogs.

**Pick something else when**

- Shallow clones as long-term copies. They depend on source files that maintenance may remove.

## Senior engineer verdict

> Shallow clone is my staging environment for table changes. Clone, run the change, compare, drop. It costs almost nothing.

## Examples

### 1. Shallow clone for a test run

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE OR REPLACE TABLE dev.sandbox.orders_test
SHALLOW CLONE main.silver.orders VERSION AS OF 230""")
```

### 2. Deep clone as an incremental backup

File: [`example_2.py`](example_2.py)

```python
# Rerunning copies only files added since the last run
spark.sql("CREATE OR REPLACE TABLE backup.silver.orders DEEP CLONE main.silver.orders")
```

## Traps and gotchas

- A clone has its own history starting at version 0; it does not carry the source time travel history.
- Deep clone reruns are incremental.
