# Arrays, maps, higher-order functions, JSON and XML

Available since ~2018 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

Spark handles nested data natively: arrays, maps and structs, with higher-order functions (`transform`, `filter`, `exists`, `aggregate`) that apply lambdas without exploding. JSON strings are parsed with `from_json` and a schema; XML is read natively with the xml format and `from_xml`.

## How it flows

1. **Nested input**: JSON, XML or Avro.
2. **Parse**: from_json, from_xml or the file reader with a schema.
3. **Transform in place**: Higher-order functions on arrays and maps.
4. **Flatten if needed**: explode or inline for row-per-item tables.

```
[Nested input] --> [Parse] --> [Transform in place] --> [Flatten if needed]
```

## When to choose it

**Choose it when**

- Nested data with a known schema.
- Array logic that would otherwise need explode and regroup.

**Pick something else when**

- Unknown or highly variable schemas: use VARIANT.

## Senior engineer verdict

> explode followed by groupBy to rebuild an array is a shuffle you can usually avoid with transform or aggregate. I reach for VARIANT when the schema is unknown and for structs when it is stable.

## Examples

### 1. Higher-order functions on arrays

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
orders = spark.createDataFrame([(1, [10.0, 25.5, 4.0])], "id int, prices array<double>")
out = orders.select("id",
    F.transform("prices", lambda p: p * 1.2).alias("with_tax"),
    F.filter("prices", lambda p: p > 5).alias("over_5"),
    F.aggregate("prices", F.lit(0.0), lambda acc, p: acc + p).alias("total"),
    F.exists("prices", lambda p: p > 20).alias("has_big_item"))
out.show(truncate=False)
```

### 2. Parse JSON strings and read XML files

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F
raw = spark.createDataFrame([('{"id": 7, "tags": ["a", "b"]}',)], "body string")
schema = F.schema_of_json(F.lit('{"id": 7, "tags": ["a"]}'))
parsed = raw.select(F.from_json("body", schema).alias("j")).select("j.id", F.explode("j.tags").alias("tag"))

books = (spark.read.format("xml").option("rowTag", "book")
    .load("/Volumes/main/landing/catalog/books.xml"))
```

## Traps and gotchas

- from_json returns null for rows that do not match the schema (or errors in FAILFAST mode).
- Lambdas in Python higher-order functions build Spark expressions; they are not executed as Python.
