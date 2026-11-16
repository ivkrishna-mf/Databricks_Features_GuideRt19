# Lakeflow Connect

**Major feature** · Available since ~2024 · DE Professional exam: S2

## What it is

Managed connectors that ingest from SaaS applications and operational databases into streaming tables. For SQL Server, MySQL and PostgreSQL, an ingestion gateway reads the change log of the source and stages changes in a Unity Catalog volume; a serverless ingestion pipeline applies them to Delta tables.

## How it flows

1. **Source database**: Change tracking or CDC enabled, with a replication user.
2. **UC connection**: Stores host and credentials.
3. **Ingestion gateway**: Runs continuously on classic compute, extracts snapshots and changes into a staging volume.
4. **Ingestion pipeline**: Serverless pipeline applies changes as SCD type 1 or type 2.
5. **Streaming tables**: Governed bronze tables, ready for silver.

```
[Source database] --> [UC connection] --> [Ingestion gateway] --> [Ingestion pipeline] --> [Streaming tables]
```

## When to choose it

**Choose it when**

- CDC from SQL Server, MySQL or PostgreSQL without building Debezium and Kafka.
- SaaS sources with a supported connector.

**Pick something else when**

- Unsupported sources or custom extraction logic: use Auto Loader, a bus, or a custom source.
- You only need occasional queries: federate.

## Senior engineer verdict

> I pick Connect whenever a connector exists, because the hard parts of CDC are operational: initial snapshot, log retention, schema changes, restarts. The cost to remember is that the gateway is always-on classic compute and the source must keep its change log long enough for outages.

## Examples

### 1. Create an ingestion pipeline with the Python SDK

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.pipelines import IngestionPipelineDefinition, IngestionConfig, TableSpec
w = WorkspaceClient()
p = w.pipelines.create(
    name="erp_ingest", catalog="main", schema="bronze_erp", serverless=True,
    ingestion_definition=IngestionPipelineDefinition(
        ingestion_gateway_id="<gateway-pipeline-id>",
        objects=[IngestionConfig(table=TableSpec(
            source_catalog="erp", source_schema="dbo", source_table="customers",
            destination_catalog="main", destination_schema="bronze_erp"))]))
w.pipelines.start_update(pipeline_id=p.pipeline_id)
```

### 2. Ingestion pipeline in a bundle

File: [`example_2.yml`](example_2.yml)

```yaml
resources:
  pipelines:
    sqlserver_ingest:
      name: sqlserver_ingest
      catalog: main
      schema: bronze_erp
      ingestion_definition:
        ingestion_gateway_id: ${resources.pipelines.erp_gateway.id}
        objects:
          - table:
              source_catalog: erp
              source_schema: dbo
              source_table: customers
              destination_catalog: main
              destination_schema: bronze_erp
              table_configuration:
                scd_type: SCD_TYPE_2
```

### 3. Read the ingested table downstream

File: [`example_3.py`](example_3.py)

```python
# SCD2 output keeps history with __START_AT and __END_AT
current = (spark.read.table("main.bronze_erp.customers")
    .where("__END_AT IS NULL"))
changes = spark.readStream.option("skipChangeCommits", "true").table("main.bronze_erp.customers")
```

## Traps and gotchas

- The gateway is not serverless; the ingestion pipeline is.
- SQL Server needs change tracking (tables with a primary key) or CDC (tables without one) enabled at the source.
