# Renames, drops and type widening

Available since ~2022 · Part of [Constraints, generated, identity and default columns](../README.md)

## What it is

Parquet files identify columns by name, so renaming used to mean rewriting data. Column mapping gives each column a stable internal id, which lets you rename and drop columns as metadata changes. Type widening lets you change a column to a wider type (int to bigint, float to double, decimal precision up) without rewriting files.

## How it flows

1. **Enable feature**: Column mapping mode name, or type widening.
2. **ALTER TABLE**: Rename, drop or widen.
3. **Metadata commit**: Schema changes; files stay.
4. **Readers**: Map old files to the new schema.

```
[Enable feature] --> [ALTER TABLE] --> [Metadata commit] --> [Readers]
```

## When to choose it

**Choose it when**

- Cleaning up badly named source columns.
- A counter outgrows INT.

**Pick something else when**

- Readers on old Delta clients: these features upgrade the table protocol.

## Senior engineer verdict

> Column mapping changes how a streaming reader sees the table: a rename or drop is a non-additive schema change, so downstream streams need a schema tracking location or a restart. I plan these changes like a migration.

## Examples

### 1. Rename and drop without rewriting data

File: [`example_1.py`](example_1.py)

```python
spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name')")
spark.sql("ALTER TABLE main.silver.orders RENAME COLUMN cust_no TO customer_id")
spark.sql("ALTER TABLE main.silver.orders DROP COLUMN legacy_flag")
```

### 2. Widen a column type

File: [`example_2.py`](example_2.py)

```python
spark.sql("ALTER TABLE main.silver.events SET TBLPROPERTIES ('delta.enableTypeWidening' = 'true')")
spark.sql("ALTER TABLE main.silver.events ALTER COLUMN view_count TYPE BIGINT")
# Streaming readers of a renamed/dropped column table:
s = (spark.readStream.option("schemaTrackingLocation", "/Volumes/main/ops/chk/events_schema")
    .table("main.silver.orders"))
```

## Traps and gotchas

- Dropping a column with column mapping does not remove its data from files until they are rewritten.
- Narrowing types (bigint to int) is never allowed in place.
