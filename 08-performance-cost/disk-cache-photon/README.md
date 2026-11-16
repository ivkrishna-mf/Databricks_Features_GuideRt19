# Disk cache, data skipping and Photon

Available since ~2018 · DE Professional exam: S5

## What it is

The disk cache (formerly Delta cache) keeps copies of remote Parquet data on the local SSDs of workers, so repeated reads of the same files skip cloud storage. Data skipping uses per-file min and max statistics to avoid reading files at all. Photon is the vectorized engine that runs SQL and DataFrame operations faster.

## How it flows

1. **First query**: Reads files from cloud storage and stores them on local SSD.
2. **Second query**: Same files are read from the local disk.
3. **File changes**: Cache detects it and refreshes automatically.
4. **Cluster stops**: The cache is gone; it is not persistent.

```
[First query] --> [Second query] --> [File changes] --> [Cluster stops]
```

## When to choose it

**Choose it when**

- Repeated reads of the same tables: BI and iterative development.
- SSD-backed workers and SQL warehouses, where it is on by default.

**Pick something else when**

- Expecting it to help write-heavy ETL that reads each file once.

## Disk cache or Spark cache

|  | Disk cache | Spark cache ([[.cache()]]) |
|---|---|---|
| Stores | Remote files on local SSD | Computed DataFrame in memory or disk |
| Triggered | Automatically on read | Manually |
| Stays correct when files change | Yes | No, must be invalidated |
| Best for | Repeated table scans | An expensive intermediate result reused in one job |

## Senior engineer verdict

> I rarely call `.cache()` on a Delta table. It pins a snapshot in memory, bypasses data skipping on later filters and competes with execution memory. The disk cache gives most of the benefit with no code.

## Examples

### 1. Check and enable the disk cache

File: [`example_1.py`](example_1.py)

```python
print(spark.conf.get("spark.databricks.io.cache.enabled"))
spark.conf.set("spark.databricks.io.cache.enabled", "true")
spark.sql("CACHE SELECT order_id, amount FROM main.gold.fact_orders WHERE order_date >= '2026-01-01'")   # preload
```

### 2. Make data skipping work for you

File: [`example_2.py`](example_2.py)

```python
# Filters on clustered columns with literal values prune files
fast = spark.table("main.silver.events").where("event_date = '2026-11-01' AND country = 'DE'")
# A function on the column hides it from file statistics
slow = spark.table("main.silver.events").where("date_format(event_date, 'yyyy-MM') = '2026-11'")
fast.explain("formatted")
```

## Traps and gotchas

- Disk cache is per cluster and lost on termination.
- Statistics are collected for a limited set of columns (the first 32 by default on external tables); long strings are poor skipping columns.
- Photon does not speed up Python UDFs or RDD code.
