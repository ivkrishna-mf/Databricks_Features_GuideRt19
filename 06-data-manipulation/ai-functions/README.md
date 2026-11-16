# AI functions and ai_query

Available since ~2023 · DE Professional exam: S3

## What it is

SQL functions that call models from inside a query. `ai_query` calls any model serving endpoint and is the general tool for batch inference. Task functions such as `ai_classify`, `ai_extract`, `ai_mask`, `ai_summarize` and `ai_analyze_sentiment` cover common jobs with no endpoint to pick.

## How it flows

1. **Rows**: Text columns in a table.
2. **ai_query**: Builds a request per row for the endpoint.
3. **Model serving**: Batched inference.
4. **Structured result**: Parsed into columns.
5. **Pipeline table**: Stored as a new column for downstream use.

```
[Rows] --> [ai_query] --> [Model serving] --> [Structured result] --> [Pipeline table]
```

## When to choose it

**Choose it when**

- Classification, extraction or enrichment as a pipeline step.
- Scoring a custom model over a table.

**Pick something else when**

- Interactive per-row use on huge tables without limits: cost scales with rows and tokens.
- Deterministic logic that a regular expression can do.

## Senior engineer verdict

> I treat model calls like any expensive external dependency: run them incrementally on new rows only (a streaming table or change feed), store the output, record the endpoint name, and return errors as data so one bad row does not fail the batch.

## Examples

### 1. Classify incrementally in a pipeline

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="silver_tickets_classified")
def silver_tickets_classified():
    return (spark.readStream.table("bronze_tickets")
        .withColumn("category",
            F.expr("ai_classify(body, array('billing', 'outage', 'how-to', 'other'))")))
```

### 2. ai_query with errors returned as data

File: [`example_2.py`](example_2.py)

```python
scored = spark.sql("""
SELECT ticket_id,
       ai_query('databricks-meta-llama-3-3-70b-instruct',
                concat('Extract the product name from: ', body),
                failOnError => false) AS r
FROM main.silver.tickets""")
ok = scored.selectExpr("ticket_id", "r.result AS product", "r.errorMessage AS error")
```

## Traps and gotchas

- With `failOnError => false` the result is a struct with the response and an error message.
- AI functions are not deterministic; do not put them in a view that is recomputed on every read.
