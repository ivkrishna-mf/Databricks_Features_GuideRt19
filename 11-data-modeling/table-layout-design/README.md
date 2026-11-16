# Designing Delta and Iceberg table layouts

Available since ~2023 · DE Professional exam: S9

## What it is

Layout design has three levers. Partitioning should match the grain at which data is managed (if at all). Clustering should match how data is filtered and joined. Compaction should keep files large enough to scan efficiently and small enough to skip.

## How it flows

1. **Know the grain**: One row per what?
2. **Know the access pattern**: Top filters and join keys.
3. **Choose clustering**: Liquid clustering on those keys, or AUTO.
4. **Choose format**: Delta by default; Iceberg or UniForm when other engines read it.
5. **Automate upkeep**: Managed tables plus predictive optimization.

```
[Know the grain] --> [Know the access pattern] --> [Choose clustering] --> [Choose format] --> [Automate upkeep]
```

## When to choose it

**Choose it when**

- At table creation, and again when query patterns change.

**Pick something else when**

- Partitioning by a timestamp or id.
- Tuning file size by hand before measuring.

## Senior engineer verdict

> I ask who reads the table and how, not what the source looked like. Facts cluster by date and the main join key; dimensions cluster by their key. When Snowflake, Trino or another engine must read it, I keep one copy and expose it through Iceberg reads, so there is no second pipeline to maintain.

## Examples

### 1. Fact table clustered for its access pattern

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE TABLE main.gold.fact_orders (
  order_id BIGINT, customer_sk BIGINT, store_sk BIGINT,
  order_date DATE, amount DECIMAL(18,2))
CLUSTER BY (order_date, customer_sk)
TBLPROPERTIES ('delta.targetFileSize' = '256mb')""")
```

### 2. One table readable as Delta and Iceberg

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
ALTER TABLE main.gold.fact_orders SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg')""")
# A managed Iceberg table instead
spark.sql("CREATE TABLE main.gold.dim_store_ice (store_sk BIGINT, name STRING) USING ICEBERG")
```

## Traps and gotchas

- Over-partitioning creates many small files and slows planning.
- UniForm writes Iceberg metadata for the same data files; it is not a copy.
