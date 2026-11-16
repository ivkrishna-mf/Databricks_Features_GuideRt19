# Predictive optimization, OPTIMIZE and VACUUM

**Major feature** · Available since ~2023 · DE Professional exam: S5

## What it is

OPTIMIZE compacts small files and applies clustering. VACUUM deletes files no longer referenced and older than the retention period. ANALYZE collects statistics. Predictive optimization runs all three automatically for Unity Catalog managed tables, choosing when it pays off.

## How it flows

1. **Writes create small files**: Especially streaming and MERGE.
2. **Predictive optimization**: Decides per table what is worth running.
3. **OPTIMIZE**: Compacts and clusters.
4. **ANALYZE**: Refreshes statistics for the optimizer.
5. **VACUUM**: Removes unreferenced files past retention; storage cost drops.

```
[Writes create small files] --> [Predictive optimization] --> [OPTIMIZE] --> [ANALYZE] --> [VACUUM]
```

## When to choose it

**Choose it when**

- Managed tables: enable predictive optimization at account, catalog or schema level and stop scheduling maintenance jobs.
- External tables: schedule OPTIMIZE and VACUUM yourself.

**Pick something else when**

- VACUUM with a retention shorter than your longest running query or stream lag.

## Senior engineer verdict

> Scheduled OPTIMIZE and VACUUM notebooks are legacy on managed tables. I enable predictive optimization, check `system.storage.predictive_optimization_operations_history` to see what it did, and only tune write-time settings such as optimized writes where streaming creates many tiny files.

## Examples

### 1. Enable for a catalog and inspect what ran

File: [`example_1.py`](example_1.py)

```python
spark.sql("ALTER CATALOG main ENABLE PREDICTIVE OPTIMIZATION")
(spark.table("system.storage.predictive_optimization_operations_history")
    .where("catalog_name = 'main'")
    .groupBy("operation_type").count().show())
```

### 2. Manual maintenance for an external table

File: [`example_2.py`](example_2.py)

```python
spark.sql("OPTIMIZE main.raw.partner_feed")
spark.sql("ALTER TABLE main.raw.partner_feed SET TBLPROPERTIES ("
          "'delta.autoOptimize.optimizeWrite' = 'true', 'delta.autoOptimize.autoCompact' = 'true')")
spark.sql("VACUUM main.raw.partner_feed RETAIN 168 HOURS")
```

## Traps and gotchas

- Default VACUUM retention is 7 days. After VACUUM you cannot time travel to versions whose files were removed.
- OPTIMIZE is idempotent and does not change data, but it creates new files, so storage rises until VACUUM runs.
- Predictive optimization does not apply to external tables.
