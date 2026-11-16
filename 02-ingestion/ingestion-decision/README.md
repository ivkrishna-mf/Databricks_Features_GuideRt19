# Which ingestion method to choose

**Major feature** · DE Professional exam: S2

## What it is

Ingestion questions are selection questions. Start from the source type, then latency, then how much infrastructure you are willing to own.

## How it flows

1. **What is the source?**: Files, a message bus, an operational database, a SaaS app, or another lakehouse.
2. **Is a managed connector available?**: For databases and SaaS, Lakeflow Connect comes first.
3. **Files: how many, how often?**: Auto Loader for anything continuous or large; COPY INTO for small scheduled SQL loads.
4. **Do you need the data copied at all?**: If not, federate or share instead of ingesting.
5. **Land in bronze**: A streaming table or Delta table governed by Unity Catalog.

```
[What is the source?] --> [Is a managed connector available?] --> [Files: how many, how often?] --> [Do you need the data copied at all?] --> [Land in bronze]
```

## Decision table

| Source and need | Choose | Why |
|---|---|---|
| Files in cloud storage, arriving continuously or in large numbers | Auto Loader, inside a pipeline or Structured Streaming | Incremental discovery, exactly-once, schema inference and evolution |
| A few thousand files, SQL-only team, scheduled loads | `COPY INTO` | Idempotent and simple; no stream to operate |
| Kafka, Kinesis, Pub/Sub, Event Hubs | Structured Streaming source or a pipeline streaming table | Offsets tracked in the checkpoint |
| SQL Server, MySQL, PostgreSQL changes | Lakeflow Connect database connector | Managed gateway captures CDC; no custom log readers |
| Salesforce, Workday, ServiceNow and similar | Lakeflow Connect SaaS connector | Managed API paging, incremental cursors, schema evolution |
| Occasional queries on an external database, no copy wanted | Lakehouse Federation | Query in place with pushdown and UC governance |
| Data owned by another organization or metastore | OpenSharing (Delta Sharing) | Live read access with no copy |
| Full snapshots only, no change feed | AUTO CDC FROM SNAPSHOT | Diffs snapshots into SCD1 or SCD2 |
| One-time historical load | `spark.read` then write, or COPY INTO | No state needed |

## Senior engineer verdict

> I ask three questions in this order: can a managed connector do it, can a declarative pipeline do it, and only then do I write Structured Streaming by hand. Every step down that list is more code I have to operate at 3 a.m.

## Examples

### 1. Same files, three ways: one-off, incremental, scheduled

File: [`example_1.py`](example_1.py)

```python
path = "/Volumes/main/landing/orders/"
once = spark.read.format("json").load(path)                         # one-off load, no state

incremental = (spark.readStream.format("cloudFiles")                  # Auto Loader, exactly once
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/orders/_schema")
    .load(path))

spark.sql(f"COPY INTO main.bronze.orders FROM '{path}' FILEFORMAT = JSON "
          "COPY_OPTIONS ('mergeSchema' = 'true')")                   # idempotent SQL load
```

### 2. Query in place versus copy

File: [`example_2.py`](example_2.py)

```python
# Federation: query the source directly, nothing copied
emea = spark.table("crm.public.accounts").where("region = 'EMEA'")
# Sharing: provider data mounted as a catalog, nothing copied
shared = spark.table("partner_retail.gold.daily_sales")
# Ingest when you need history, heavy joins or low query latency
emea.write.mode("overwrite").saveAsTable("main.bronze.crm_accounts_snapshot")
```

## Traps and gotchas

- Federation is for querying, not for high-volume ETL. If the scenario mentions heavy joins or dashboards with strict latency, ingest instead.
- COPY INTO and Auto Loader are both idempotent. The difference is scale, schema evolution and file discovery cost.
