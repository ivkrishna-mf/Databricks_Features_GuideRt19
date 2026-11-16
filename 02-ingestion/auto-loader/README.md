# Auto Loader

**Major feature** · Available since ~2020 · DE Professional exam: S1, S2

## What it is

Auto Loader is the `cloudFiles` Structured Streaming source. It discovers new files in cloud storage, records each one in RocksDB inside the checkpoint so it is processed exactly once, and infers and evolves the schema.

It reads JSON, CSV, Parquet, Avro, ORC, text, XML and binary files, and works the same in a notebook stream and in a Lakeflow pipeline.

## How it flows

1. **Files land**: A producer drops files into a storage path or volume.
2. **Discovery**: Directory listing, or file notifications through file events.
3. **Checkpoint state**: Each discovered file is recorded. A restart resumes without reprocessing.
4. **Schema location**: Inferred schema is stored and versioned; new columns are handled by the evolution mode.
5. **Bronze table**: Rows are appended to a Delta or streaming table.

```
[Files land] --> [Discovery] --> [Checkpoint state] --> [Schema location] --> [Bronze table]
```

## When to choose it

**Choose it when**

- Files arrive over time and you must not reload or miss any.
- The schema is unknown or drifts.
- Directories hold many thousands to billions of files.

**Pick something else when**

- A single static load: plain `spark.read` is enough.
- The source is a queue or a database: use the matching connector.

## Senior engineer verdict

> Auto Loader is my default for files, run with `availableNow` on a schedule unless the business needs minutes. Three options carry most of the weight: `cloudFiles.schemaLocation`, the schema evolution mode and the file detection mode. Inside a pipeline the checkpoint and schema location are managed for you, which is one more reason to prefer pipelines.

## Examples

### 1. Incremental JSON ingestion as a scheduled batch

File: [`example_1.py`](example_1.py)

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders/_schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("/Volumes/main/landing/orders/")
  .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/orders")
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable("main.bronze.orders"))
```

### 2. The same source inside a Lakeflow pipeline

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="bronze_orders", comment="Raw orders from landing")
def bronze_orders():
    return (spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.schemaHints", "amount DECIMAL(18,2), order_ts TIMESTAMP")
        .load("/Volumes/main/landing/orders_csv/")
        .withColumn("src_file", F.col("_metadata.file_path")))
```

## Traps and gotchas

- Without `cloudFiles.inferColumnTypes`, JSON and CSV columns are inferred as strings.
- Deleting the checkpoint makes Auto Loader reprocess every file.
- Auto Loader does not guarantee file processing order.

## Sub-features

- [File detection modes](file-detection-modes/README.md)
- [Schema inference, evolution and rescued data](auto-loader-schema/README.md)
- [Triggers, backfills and cleanup](auto-loader-operations/README.md)
