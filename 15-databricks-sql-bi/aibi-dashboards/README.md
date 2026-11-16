# AI/BI dashboards

Available since ~2024

## What it is

Dashboards built on SQL warehouses: datasets (queries or metric views), visualizations, filters and parameters, with AI-assisted chart authoring. Published dashboards can embed credentials so viewers see data without direct table access, can be scheduled to email subscribers, and are deployable through bundles.

## How it flows

1. **Datasets**: SQL queries or metric views.
2. **Widgets**: Charts, counters, tables, filters.
3. **Draft**: Edit and preview.
4. **Publish**: With the publisher's credentials or each viewer's own.
5. **Share and schedule**: Users, groups, email subscriptions, embedding.

```
[Datasets] --> [Widgets] --> [Draft] --> [Publish] --> [Share and schedule]
```

## When to choose it

**Choose it when**

- Operational and executive dashboards that live next to the data and governance.
- Teams that want dashboards versioned and deployed with the rest of the project.

**Pick something else when**

- Pixel-perfect paginated reporting: use a dedicated BI tool on the same warehouse.

## Senior engineer verdict

> Point dashboards at metric views or small gold tables, never at raw silver. Publish with embedded credentials for broad audiences so you do not have to grant table access to every viewer, and keep the dashboard JSON in the bundle so it is reviewed like code.

## Examples

### 1. Build the small gold table a dashboard should read

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
(spark.table("main.gold.fact_orders")
    .groupBy("order_date", "region")
    .agg(F.sum("amount").alias("revenue"), F.countDistinct("order_id").alias("orders"))
    .write.mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable("main.gold.dash_daily_region"))
spark.sql("COMMENT ON TABLE main.gold.dash_daily_region IS 'Feeds the Sales overview dashboard'")
```

### 2. Deploy a dashboard with a bundle

File: [`example_2.yml`](example_2.yml)

```yaml
resources:
  dashboards:
    sales_overview:
      display_name: "Sales overview"
      file_path: ../src/dashboards/sales_overview.lvdash.json
      warehouse_id: ${var.bi_warehouse_id}
      embed_credentials: true
      permissions:
        - group_name: sales_team
          level: CAN_VIEW
```

### 3. Publish and list dashboards with the SDK

File: [`example_3.py`](example_3.py)

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
d = next(x for x in w.lakeview.list() if x.display_name == "Sales overview")
w.lakeview.publish(dashboard_id=d.dashboard_id, warehouse_id="<warehouse-id>", embed_credentials=True)
print(d.dashboard_id, d.lifecycle_state)
```

## Traps and gotchas

- Embedded credentials mean viewers see what the publisher can see. Choose the publisher identity carefully.
