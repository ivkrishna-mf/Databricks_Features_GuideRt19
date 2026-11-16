# Liquid clustering, partitioning and ZORDER

**Major feature** · Available since ~2023 · DE Professional exam: S5, S9

## What it is

All three co-locate related data so queries skip files. Partitioning splits a table into directories by column value. ZORDER rewrites files to cluster by columns within a partition. Liquid clustering clusters incrementally, lets you change keys without rewriting the table, and with `CLUSTER BY AUTO` picks keys from query history.

## How it flows

1. **Rows written**: Into files tagged with min and max statistics.
2. **OPTIMIZE**: Groups rows by the clustering keys, incrementally.
3. **Query with a filter**: Engine compares the filter with file statistics.
4. **Skip files**: Only matching files are read.
5. **Keys change**: ALTER TABLE CLUSTER BY; new data follows the new keys.

```
[Rows written] --> [OPTIMIZE] --> [Query with a filter] --> [Skip files] --> [Keys change]
```

## When to choose it

**Choose it when**

- Liquid: every new table. Up to four keys; start with the most common filter columns.
- `CLUSTER BY AUTO`: managed tables where query patterns vary and you do not want to choose.

**Pick something else when**

- Partitioning tables under about a terabyte or on high-cardinality columns.
- Adding ZORDER to a liquid clustered table: not allowed.

## Comparison

|  | Liquid clustering | Partitioning | ZORDER |
|---|---|---|---|
| Best for | Most tables; high-cardinality or changing filters | Very large tables with a low-cardinality column used in nearly every query, or lifecycle by partition | Legacy tables you cannot convert yet |
| Change keys | Yes, no rewrite | No, rewrite the table | Yes, but full rewrite on next OPTIMIZE |
| Maintenance | Incremental; automatic with predictive optimization | None, but small files per partition | Not incremental; reruns are expensive |
| Skew and cardinality | Handles both | High cardinality creates tiny files | Fine for high cardinality |
| Combine | Not with partitioning or ZORDER | With ZORDER | With partitioning |

## Senior engineer verdict

> New table: liquid clustering, and AUTO if it is a managed table with predictive optimization. I keep partitioning only where something depends on it, such as dropping a whole day as a metadata operation or an external reader that expects directories. If a question mentions changing query patterns, skewed keys or 'no rewrite', the answer is liquid clustering.

## Examples

### 1. Create, change keys and optimize

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE TABLE main.silver.events (event_id STRING, user_id STRING, event_date DATE, country STRING)
CLUSTER BY (event_date, user_id)""")
spark.sql("ALTER TABLE main.silver.events CLUSTER BY (country, event_date)")
spark.sql("OPTIMIZE main.silver.events")            # incremental
spark.sql("OPTIMIZE main.silver.events FULL")       # recluster existing data to new keys
```

### 2. Automatic keys, and clustering from the DataFrame API

File: [`example_2.py`](example_2.py)

```python
spark.sql("ALTER TABLE main.silver.orders CLUSTER BY AUTO")

(df.write.mode("overwrite")
    .clusterBy("order_date", "customer_id")
    .saveAsTable("main.silver.orders_v2"))
```

## Traps and gotchas

- `CLUSTER BY AUTO` requires a Unity Catalog managed table with predictive optimization.
- ZORDER BY cannot use partition columns, and is ignored for data written after the last OPTIMIZE.
- Clustering keys must have statistics collected (within the indexed columns).
