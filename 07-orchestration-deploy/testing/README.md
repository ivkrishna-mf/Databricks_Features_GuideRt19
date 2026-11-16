# Unit and integration testing

Available since ~2023 · DE Professional exam: S1

## What it is

Testable pipelines keep transformations as functions from DataFrame to DataFrame. `pyspark.testing` gives `assertDataFrameEqual` and `assertSchemaEqual`. `DataFrame.transform` chains those functions in production code.

## How it flows

1. **Pure function**: Takes a DataFrame, returns a DataFrame. No reads or writes inside.
2. **Unit test**: Small in-memory input, expected output, assert equal.
3. **Compose**: `df.transform(f).transform(g)` in the job or pipeline.
4. **Integration test**: Deploy the bundle to a test target and run on sample data.
5. **CI gate**: Both must pass before deploy.

```
[Pure function] --> [Unit test] --> [Compose] --> [Integration test] --> [CI gate]
```

## When to choose it

**Choose it when**

- Always for business logic. Bugs in joins and window logic are cheap to catch here.

**Pick something else when**

- Tests that depend on production tables or on row order.

## Senior engineer verdict

> If a transformation cannot be tested without a cluster and a real table, the design is the problem. I separate I/O from logic, test logic with ten-row DataFrames, and use expectations plus a small integration run for everything else.

## Examples

### 1. Transformations as functions, chained with transform

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import DataFrame, functions as F

def with_net(df: DataFrame, rate: float) -> DataFrame:
    return df.withColumn("net", F.round(F.col("gross") / (1 + rate), 2))

def only_paid(df: DataFrame) -> DataFrame:
    return df.where("status = 'PAID'")

silver = spark.table("main.bronze.orders").transform(only_paid).transform(with_net, 0.2)
```

### 2. pytest unit test

File: [`example_2.py`](example_2.py)

```python
from pyspark.testing import assertDataFrameEqual, assertSchemaEqual
from orders.transforms import with_net, only_paid

def test_net_for_paid_orders(spark):
    src = spark.createDataFrame([(1, "PAID", 120.0), (2, "OPEN", 60.0)], "id int, status string, gross double")
    out = src.transform(only_paid).transform(with_net, 0.2)
    expected = spark.createDataFrame([(1, "PAID", 120.0, 100.0)], "id int, status string, gross double, net double")
    assertSchemaEqual(out.schema, expected.schema)
    assertDataFrameEqual(out, expected)          # ignores row order by default
```

## Traps and gotchas

- `assertDataFrameEqual` ignores row order unless `checkRowOrder=True`.
- Floats compare with a tolerance (`rtol`, `atol`).
