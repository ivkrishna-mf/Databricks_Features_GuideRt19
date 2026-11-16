# Migrating from Hive metastore to Unity Catalog

Available since ~2023

## What it is

Older workspaces keep tables in the workspace-local Hive metastore. Moving to Unity Catalog unlocks serverless, lineage, ABAC, sharing and predictive optimization. Options: SYNC upgrades external tables in place, CLONE or CTAS copies managed tables, HMS federation exposes the legacy metastore in Unity Catalog during a gradual move, and the UCX tool from Databricks Labs automates assessment and migration.

## How it flows

1. **Assess**: UCX inventory: tables, mounts, jobs, incompatible code.
2. **Set up UC**: Metastore, credentials, external locations, groups.
3. **Move tables**: SYNC external tables; DEEP CLONE or CTAS managed ones.
4. **Repoint code**: Three-level names, volumes instead of mounts.
5. **Switch and lock**: Run jobs on UC-enabled compute; make HMS read-only.

```
[Assess] --> [Set up UC] --> [Move tables] --> [Repoint code] --> [Switch and lock]
```

## When to choose it

**Choose it when**

- Any workspace still running on the Hive metastore.

**Pick something else when**

- A big-bang cutover without an inventory of jobs and mounts.

## Senior engineer verdict

> The tables are the easy part. The work is in code: mount paths, two-level names, RDD usage that fails on standard access mode, and init scripts. Run the assessment first and fix code in parallel with moving data.

## Examples

### 1. Upgrade external tables in place with SYNC

File: [`example_1.py`](example_1.py)

```python
spark.sql("SYNC SCHEMA main.sales FROM hive_metastore.sales DRY RUN").show(truncate=False)
spark.sql("SYNC SCHEMA main.sales FROM hive_metastore.sales")
spark.sql("SYNC TABLE main.sales.orders FROM hive_metastore.sales.orders")   # single table
```

### 2. Copy a managed table and install UCX

File: [`example_2.py`](example_2.py)

```python
spark.sql("CREATE TABLE main.sales.customers DEEP CLONE hive_metastore.sales.customers")
spark.sql("ALTER TABLE hive_metastore.sales.customers SET TBLPROPERTIES ('upgraded_to' = 'main.sales.customers')")
# Shell, on your machine:
#   databricks labs install ucx
#   databricks labs ucx ensure-assessment-run
```

## Traps and gotchas

- SYNC works for external tables; managed HMS tables must be copied.
- After migration, jobs must run on compute with standard or dedicated access mode.
