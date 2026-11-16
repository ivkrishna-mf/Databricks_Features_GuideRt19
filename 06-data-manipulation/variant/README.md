# VARIANT for semi-structured data

Available since ~2024 · DE Professional exam: S3

## What it is

VARIANT stores JSON-like data in a binary encoded form that keeps the original types and structure without a fixed schema. It is faster to query than JSON strings and more flexible than structs.

## How it flows

1. **Raw JSON string**: From files or a message bus.
2. **parse_json**: Becomes a VARIANT value.
3. **Store**: One column in bronze.
4. **Extract**: `variant_get` or the `:` path syntax with a cast.
5. **Typed silver**: Promote stable fields to real columns.

```
[Raw JSON string] --> [parse_json] --> [Store] --> [Extract] --> [Typed silver]
```

## When to choose it

**Choose it when**

- Schemas that change often or differ per record.
- You want to land everything and decide types later.

**Pick something else when**

- Stable, well-known fields that are filtered or joined often: typed columns give better statistics and pruning.

## Senior engineer verdict

> VARIANT in bronze, typed columns in silver. It removed most of my schema evolution failures in ingestion. I use `try_variant_get` in pipelines so one malformed value does not fail a batch.

## Examples

### 1. Parse, store and extract

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
raw = spark.table("main.bronze.events_raw")                 # column: body STRING
v = raw.select(F.parse_json("body").alias("payload"))
out = v.select(
    F.variant_get("payload", "$.user.id", "string").alias("user_id"),
    F.try_variant_get("payload", "$.cart.total", "decimal(18,2)").alias("total"))
```

### 2. Path syntax and exploding an array

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
SELECT payload:order_id::string AS order_id,
       item.value:sku::string   AS sku,
       item.value:qty::int      AS qty
FROM main.bronze.orders_v,
     LATERAL variant_explode(payload:items) AS item""").show()
```

## Traps and gotchas

- `variant_get` raises on an invalid cast; `try_variant_get` returns null.
- `parse_json` fails on malformed JSON; `try_parse_json` returns null.
- Paths are case sensitive.
