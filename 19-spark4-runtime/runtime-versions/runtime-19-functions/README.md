# New SQL and DataFrame features in Runtime 19

Available since ~2026 · DBR 19 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

Runtime 19 adds functions and write options that remove boilerplate: `truncate` cuts a number to a scale without rounding, `trim_array` removes elements from either end of an array, `variant_strip_nulls` removes null fields from VARIANT objects, `SET PATH` sets the search path for unqualified function names, `INSERT INTO ... REPLACE ON / USING` replaces matching rows, and `withSchemaEvolution()` lets a DataFrame write evolve the table schema.

## How it flows

1. **Write staged data**: A day of corrected rows.
2. **INSERT ... REPLACE USING**: Rows for matching keys are replaced atomically.
3. **Schema evolution**: New columns added through withSchemaEvolution.
4. **Clean values**: truncate, trim_array, variant_strip_nulls.
5. **Downstream**: Automatic change data feed exposes the changes.

```
[Write staged data] --> [INSERT ... REPLACE USING] --> [Schema evolution] --> [Clean values] --> [Downstream]
```

## When to choose it

**Choose it when**

- Reprocessing a slice of a table (a day, a region) without a MERGE.
- Cleaning semi-structured payloads.

**Pick something else when**

- Relying on these in code that must also run on older runtimes.

## Senior engineer verdict

> INSERT REPLACE replaces the delete-then-insert pattern I used for idempotent reprocessing of a partition-like slice, and it is atomic. I still use MERGE when the match logic is row by row.

## Examples

### 1. New functions in SQL expressions

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
df = spark.createDataFrame([(3.98765, [1, 2, 3, 4, 5], '{"a": 1, "b": null}')],
                           "x double, arr array<int>, j string")
df.select(F.expr("truncate(x, 2)").alias("truncated"),            # 3.98, no rounding
          F.expr("trim_array(arr, 2)").alias("drop_last_2"),       # [1, 2, 3]
          F.expr("trim_array(arr, -1)").alias("drop_first_1"),     # [2, 3, 4, 5]
          F.expr("variant_strip_nulls(parse_json(j))").alias("clean")).show(truncate=False)
```

### 2. Replace a slice and evolve the schema on write

File: [`example_2.py`](example_2.py)

```python
corrected = spark.table("main.staging.orders_2026_11_15")
corrected.createOrReplaceTempView("corrected")
spark.sql("""
INSERT INTO main.silver.orders REPLACE USING (order_date)
SELECT * FROM corrected""")

(new_rows.writeTo("main.silver.orders")
    .withSchemaEvolution()     # DataFrame writer schema evolution (Runtime 19)
    .append())
spark.sql("SET PATH = main.fn, system.builtin")   # unqualified function names resolve in main.fn first
```

## Traps and gotchas

- REPLACE USING matches on the listed columns; every target row with a matching value is replaced, not merged.
- truncate does not round: truncate(2.999, 2) is 2.99.
