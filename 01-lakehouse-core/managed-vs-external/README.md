# Managed and external tables

Available since ~2022 · DE Professional exam: S5, S7

## What it is

A managed table lets Unity Catalog own the storage path and lifecycle. An external table points at a path you manage through an external location. Managed tables get predictive optimization, automatic statistics and faster metadata by default.

## How it flows

1. **CREATE TABLE**: No LOCATION clause means managed.
2. **UC picks storage**: Files go under the managed location of the schema, catalog or metastore.
3. **Automatic upkeep**: Predictive optimization runs OPTIMIZE, VACUUM and ANALYZE.
4. **DROP TABLE**: Managed data is deleted after the UNDROP window. External files stay.

```
[CREATE TABLE] --> [UC picks storage] --> [Automatic upkeep] --> [DROP TABLE]
```

## When to choose it

**Choose it when**

- Default for every new table.
- You want maintenance handled for you and lower cost over time.

**Pick something else when**

- Another system must write to the same path directly.
- A hard requirement to keep files after the table is dropped.

## Senior engineer verdict

> External tables are for interoperability, not for feeling safe. If a non-Databricks writer needs the data, I would rather share it through Iceberg reads or sharing than give up managed table features.

## Examples

### 1. Managed table with automatic clustering

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE TABLE main.silver.events (
  event_id STRING, user_id STRING, event_ts TIMESTAMP, payload VARIANT)
CLUSTER BY AUTO""")
```

### 2. External table on an external location

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
CREATE TABLE main.raw.partner_feed (id STRING, body STRING)
LOCATION 's3://partner-bucket/feed/'""")
# Dropping it removes metadata only; files remain in the bucket
spark.sql("DROP TABLE main.raw.partner_feed")
```

## Traps and gotchas

- Predictive optimization and `CLUSTER BY AUTO` need Unity Catalog managed tables.
- Dropping a managed table removes data; UNDROP works for a limited window (7 days by default).
