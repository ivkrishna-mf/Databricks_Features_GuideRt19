# Expectations (data quality)

Available since ~2021 · DE Professional exam: S3 · Part of [Lakeflow Spark Declarative Pipelines (SDP)](../README.md)

## What it is

An expectation is a named boolean condition on a dataset. Each row is checked and the pipeline records pass and fail counts in the event log. The action decides what happens to failing rows.

## How it flows

1. **Row arrives**: From the dataset query.
2. **Check constraint**: For example `amount > 0`.
3. **Action**: Warn keeps the row, drop removes it, fail stops the update.
4. **Metrics**: Counts go to the event log and the pipeline UI.
5. **Quarantine (pattern)**: Invert the rules into a second table to keep rejected rows.

```
[Row arrives] --> [Check constraint] --> [Action] --> [Metrics] --> [Quarantine (pattern)]
```

## When to choose it

**Choose it when**

- Warn: track a metric you are not ready to enforce.
- Drop: bad rows must not reach consumers.
- Fail: a violation means the load itself is wrong, such as a missing key in a finance table.

**Pick something else when**

- Cross-row checks such as uniqueness in a single expectation; build a materialized view that computes the check and put the expectation on that.

## Actions

| Decorator | SQL | Failing row | Update |
|---|---|---|---|
| `@dp.expect` | `CONSTRAINT c EXPECT (...)` | Kept | Continues |
| `@dp.expect_or_drop` | `... ON VIOLATION DROP ROW` | Dropped | Continues |
| `@dp.expect_or_fail` | `... ON VIOLATION FAIL UPDATE` | Not written | Fails and rolls back |

## Senior engineer verdict

> Drop without quarantine is data loss with a metric attached. In silver I define the rules once as a dictionary, apply them with `expect_all_or_drop`, and feed a quarantine table with the negated condition so someone can fix and replay.

## Examples

### 1. Rules as a dictionary: drop bad rows

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
rules = {"valid_id": "order_id IS NOT NULL",
         "positive_amount": "amount > 0",
         "known_currency": "currency IN ('USD','EUR','GBP')"}

@dp.table(name="silver_orders")
@dp.expect_all_or_drop(rules)
def silver_orders():
    return spark.readStream.table("bronze_orders")
```

### 2. Quarantine the rejected rows

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F
quarantine_cond = "NOT(" + " AND ".join("(" + r + ")" for r in rules.values()) + ")"

@dp.table(name="quarantine_orders")
def quarantine_orders():
    return (spark.readStream.table("bronze_orders")
        .where(F.expr(quarantine_cond) | F.expr("order_id IS NULL")))
```

## Traps and gotchas

- Expectations need the Advanced edition or serverless.
- `expect_or_fail` rolls back the flow; fix the data and rerun.
- Rows where the condition evaluates to NULL count as failing, so write null-safe rules.
