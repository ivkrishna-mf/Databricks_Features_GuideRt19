# pandas API on Spark and pandas functions

Available since ~2021 · Part of [How Spark executes your code](../README.md)

## What it is

The pandas API on Spark (`pyspark.pandas`) gives a pandas-like interface that runs distributed. For custom per-group or per-batch Python logic, `applyInPandas` and `mapInPandas` hand each group or batch to your function as a real pandas DataFrame.

## How it flows

1. **Distributed data**: A Spark DataFrame.
2. **Split**: By group key or into Arrow batches.
3. **Your pandas code**: Runs on executors, one group or batch at a time.
4. **Recombine**: Results form a new Spark DataFrame.

```
[Distributed data] --> [Split] --> [Your pandas code] --> [Recombine]
```

## When to choose it

**Choose it when**

- Porting pandas code to large data with minimal rewrite.
- Per-group work such as fitting a model per store.

**Pick something else when**

- Code that depends on row order or a global index on huge data.
- Groups larger than executor memory.

## Senior engineer verdict

> I use pyspark.pandas for migration, then rewrite hot paths in plain DataFrame code. applyInPandas is the workhorse for many-models training: one model per key, in parallel, with no driver bottleneck.

## Examples

### 1. pandas syntax, distributed

File: [`example_1.py`](example_1.py)

```python
import pyspark.pandas as ps
psdf = ps.read_table("main.silver.orders")
summary = (psdf[psdf["amount"] > 0]
    .groupby("country")["amount"].agg(["sum", "mean", "count"])
    .sort_values("sum", ascending=False))
summary.head(10)
sdf = psdf.to_spark()      # back to a Spark DataFrame
```

### 2. One forecast per store with applyInPandas

File: [`example_2.py`](example_2.py)

```python
import pandas as pd
def fit_store(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.sort_values("day")
    trend = pdf["sales"].rolling(7, min_periods=1).mean().iloc[-1]
    return pd.DataFrame({"store_id": [pdf["store_id"].iloc[0]], "next_day_forecast": [trend]})

forecasts = (spark.table("main.silver.daily_sales")
    .groupBy("store_id")
    .applyInPandas(fit_store, schema="store_id string, next_day_forecast double"))
```

## Traps and gotchas

- applyInPandas loads a whole group into memory on one executor.
- pyspark.pandas default index can trigger expensive operations; set a distributed index type for large data.
