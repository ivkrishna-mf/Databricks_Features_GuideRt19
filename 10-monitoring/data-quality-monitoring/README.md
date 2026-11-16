# Data quality monitoring (anomaly detection and profiling)

Available since ~2023 · DE Professional exam: S4

## What it is

Data quality monitoring has two parts. Anomaly detection is enabled per schema and checks every table for freshness (updated when expected) and completeness (expected row volume), learning normal patterns from history; results land in `system.data_quality_monitoring.table_results`. Data profiling, formerly Lakehouse Monitoring, computes statistics and drift for a chosen table into profile and drift metric tables with a generated dashboard; it also monitors inference tables of models.

## How it flows

1. **Enable on schema**: Anomaly detection scans tables, important ones first.
2. **Learn patterns**: Historical commit times and row counts.
3. **Flag issues**: Stale or incomplete tables, with upstream root cause from lineage.
4. **Profile key tables**: Statistics and drift per time window.
5. **Alert**: SQL alerts on the result tables.

```
[Enable on schema] --> [Learn patterns] --> [Flag issues] --> [Profile key tables] --> [Alert]
```

## When to choose it

**Choose it when**

- Anomaly detection: broad coverage of a whole schema with no configuration.
- Profiling: deep statistics and drift on the tables and models that matter most.

**Pick something else when**

- Replacing pipeline expectations: monitoring tells you after the fact, expectations stop bad rows at write time.

## Senior engineer verdict

> I layer it: expectations in the pipeline for rules I know, anomaly detection on every gold schema for the problems I did not think of (a source that silently stopped), and profiling on a few critical tables and model inference tables for drift.

## Examples

### 1. Read anomaly detection results

File: [`example_1.py`](example_1.py)

```python
issues = spark.sql("""
SELECT *
FROM system.data_quality_monitoring.table_results
WHERE catalog_name = 'main' AND schema_name = 'gold'
ORDER BY event_time DESC
LIMIT 50""")
issues.show(truncate=False)
```

### 2. Create a time series profile and query drift

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import MonitorTimeSeries
w = WorkspaceClient()
w.quality_monitors.create(
    table_name="main.gold.fact_orders",
    assets_dir="/Workspace/Shared/monitors/fact_orders",
    output_schema_name="main.monitoring",
    time_series=MonitorTimeSeries(timestamp_col="order_ts", granularities=["1 day"]))

spark.table("main.monitoring.fact_orders_drift_metrics").where("column_name = 'amount'").show()
```

## Traps and gotchas

- Enabling anomaly detection needs MANAGE on the schema or catalog.
- Profiling writes metric tables to the output schema you choose; it does not modify the monitored table.
