# Spark 4 SQL: ANSI mode, pipe syntax, collations

Available since ~2025 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

Spark 4 made SQL stricter and more expressive. ANSI mode is on by default, so invalid casts, overflow and division by zero raise errors instead of returning null. SQL pipe syntax (`|>`) writes queries top to bottom in the order they run. Collations make string comparison case- or accent-insensitive per column.

## How it flows

1. **FROM table**: Pipe syntax starts with the source.
2. **|> WHERE**: Filter.
3. **|> AGGREGATE**: Group and aggregate.
4. **|> ORDER BY**: Sort.
5. **Result**: Same plan as the classic query.

```
[FROM table] --> [|> WHERE] --> [|> AGGREGATE] --> [|> ORDER BY] --> [Result]
```

## When to choose it

**Choose it when**

- ANSI: always, it surfaces data bugs early.
- Pipe syntax: long analytical queries that are easier to read as steps.
- Collations: matching names or codes regardless of case.

**Pick something else when**

- Turning ANSI mode off globally to make an old job pass; fix the casts with try_ functions instead.

## Senior engineer verdict

> ANSI mode broke a few of my jobs during upgrades, and each time it had found a real data problem. `try_cast`, `try_divide` and `try_to_number` are the right fix where nulls are acceptable.

## Examples

### 1. ANSI errors and the try_ functions

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
print(spark.conf.get("spark.sql.ansi.enabled"))     # true on Spark 4 runtimes
df = spark.createDataFrame([("12",), ("abc",)], "v string")
safe = df.select(F.expr("try_cast(v AS INT)").alias("as_int"),
                 F.expr("try_divide(10, 0)").alias("ratio"))
safe.show()      # nulls instead of errors
# df.select(F.col("v").cast("int")).collect()   -> raises CAST_INVALID_INPUT under ANSI
```

### 2. Pipe syntax and a case-insensitive collation

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
FROM main.silver.orders
|> WHERE order_date >= DATE'2026-10-01'
|> AGGREGATE SUM(amount) AS revenue GROUP BY country
|> ORDER BY revenue DESC
|> LIMIT 10""").show()

spark.sql("CREATE TABLE IF NOT EXISTS main.ref.cities (name STRING COLLATE UTF8_LCASE)")
spark.sql("SELECT * FROM main.ref.cities WHERE name = 'PARIS'").show()   # matches 'Paris'
```

## Traps and gotchas

- Under ANSI, `cast` of a bad string fails the query; `try_cast` returns null.
- Collation is part of the column type; comparing columns with different collations needs an explicit COLLATE.
