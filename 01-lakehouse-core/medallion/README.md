# Medallion architecture

Available since ~2020 · DE Professional exam: S1, S9

## What it is

A layering convention. Bronze keeps raw data as it arrived, silver holds cleaned and conformed records, gold holds business-level aggregates and dimensional models. Each layer is a set of Delta tables.

## How it flows

1. **Sources**: Files, message buses, databases, SaaS.
2. **Bronze**: Append-only, raw, with ingestion metadata. Replayable.
3. **Silver**: Deduplicated, typed, validated, CDC applied. One row per business entity or event.
4. **Gold**: Aggregates, dimensions and facts for BI and ML.
5. **Consumers**: Dashboards, metric views, sharing, models.

```
[Sources] --> [Bronze] --> [Silver] --> [Gold] --> [Consumers]
```

## When to choose it

**Choose it when**

- You want to reprocess after a bug without going back to the source.
- Different teams need different trust levels of the same data.

**Pick something else when**

- A tiny one-off dataset. Three copies add cost with no gain.

## Senior engineer verdict

> Keep bronze dumb. The moment you filter or cast in bronze, you lose the ability to replay. I add `_metadata.file_path`, an ingest timestamp and the rescued data column, and nothing else.

## Examples

### 1. Bronze: raw plus metadata

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
bronze = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders_schema")
    .load("/Volumes/main/landing/orders/")
    .select("*", F.col("_metadata.file_path").alias("src_file"),
            F.current_timestamp().alias("ingested_at")))
```

### 2. Silver: type, validate, deduplicate

File: [`example_2.py`](example_2.py)

```python
silver = (spark.readStream.table("main.bronze.orders")
    .withColumn("order_ts", F.to_timestamp("order_ts"))
    .where("order_id IS NOT NULL")
    .withWatermark("order_ts", "1 hour")
    .dropDuplicatesWithinWatermark(["order_id"]))
(silver.writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/orders_silver")
    .trigger(availableNow=True).toTable("main.silver.orders"))
```

## Traps and gotchas

- Bronze is append-only. Applying updates there breaks downstream streaming reads unless they set `skipChangeCommits`.
