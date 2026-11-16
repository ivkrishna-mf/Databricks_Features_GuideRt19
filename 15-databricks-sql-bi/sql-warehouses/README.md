# SQL warehouses

**Major feature** · Available since ~2020

## What it is

A SQL warehouse is compute for SQL: the SQL editor, dashboards, Genie, alerts, BI tools over JDBC or ODBC, and SQL tasks in jobs. Serverless warehouses start in seconds, scale out by adding clusters when queries queue, and use Photon and intelligent workload management.

## How it flows

1. **Query arrives**: From a tool, dashboard or API.
2. **Queue and route**: Workload management schedules it.
3. **Scale**: More clusters are added under concurrency, up to the maximum.
4. **Execute**: Photon, disk cache and result cache.
5. **Auto stop**: The warehouse stops after idle minutes.

```
[Query arrives] --> [Queue and route] --> [Scale] --> [Execute] --> [Auto stop]
```

## When to choose it

**Choose it when**

- Any SQL-only workload, especially many concurrent users.

**Pick something else when**

- Python or ML workloads: use serverless notebooks and jobs.

## Types

| Type | Start time | Choose when |
|---|---|---|
| Serverless | Seconds | Default: BI, ad hoc SQL, dashboards, Genie |
| Pro | Minutes | Serverless not available, or features that need your own network |
| Classic | Minutes | Legacy; few reasons to pick it now |

## Senior engineer verdict

> Size for the heaviest single query (the T-shirt size), scale for concurrency (max clusters). I separate warehouses by workload, such as BI, ad hoc and ETL, so one runaway query cannot slow the CEO dashboard, and I tag each one for cost reporting.

## Examples

### 1. Create a serverless warehouse with the SDK

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType, EndpointTags, EndpointTagPair
w = WorkspaceClient()
wh = w.warehouses.create(
    name="bi-serverless", cluster_size="Small",
    min_num_clusters=1, max_num_clusters=4, auto_stop_mins=10,
    enable_serverless_compute=True,
    warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
    tags=EndpointTags(custom_tags=[EndpointTagPair(key="team", value="bi")])).result()
print(wh.id)
```

### 2. Run SQL from any app with the Statement Execution API

File: [`example_2.py`](example_2.py)

```python
resp = w.statement_execution.execute_statement(
    warehouse_id=wh.id,
    statement="SELECT region, SUM(amount) AS revenue FROM main.gold.fact_orders WHERE order_date >= :d GROUP BY region",
    parameters=[{"name": "d", "value": "2026-11-01", "type": "DATE"}],
    wait_timeout="30s")
print(resp.status.state, resp.result.data_array[:5])
```

## Traps and gotchas

- Serverless warehouses require serverless enabled for the workspace.
- The result cache returns identical query results without recomputing when the data has not changed.

## Sub-features

- [Parameterized SQL and SQL scripting](sql-scripting-params/README.md)
