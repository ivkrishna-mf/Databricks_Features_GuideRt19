# Dimensional models, materialized views and metric views

**Major feature** · Available since ~2025 · DE Professional exam: S9

## What it is

Gold is usually a star schema: fact tables of events with numeric measures, and dimension tables that describe them. Materialized views precompute heavy aggregations so dashboards read small results. Metric views define measures and dimensions once in Unity Catalog so every tool computes a metric the same way.

## How it flows

1. **Silver entities**: Clean orders, customers, products.
2. **Dimensions**: Surrogate keys, SCD type as required.
3. **Facts**: Keys to dimensions plus measures.
4. **Materialized views**: Pre-aggregated for known heavy queries.
5. **Metric views**: Governed definitions queried with `MEASURE()`.

```
[Silver entities] --> [Dimensions] --> [Facts] --> [Materialized views] --> [Metric views]
```

## When to choose it

**Choose it when**

- Star schema for BI.
- Materialized view for stable, expensive aggregates.
- Metric view for KPIs that must mean one thing.

**Pick something else when**

- One wide table for everything when dimensions change independently.
- Storing ratios in a materialized view and averaging them later.

## Materialized view or metric view

|  | Materialized view | Metric view |
|---|---|---|
| What it is | Stored query result | Semantic definition: dimensions and measures in YAML |
| Computes | At refresh | At query time, at whatever grain is asked |
| Solves | Speed of a fixed aggregation | One governed definition of a metric, including ratios and distinct counts that cannot be re-aggregated |
| Choose when | A dashboard runs the same expensive aggregation | Many teams slice the same KPI differently |

## Senior engineer verdict

> I declare primary and foreign keys on gold tables even though they are informational: the optimizer and BI tools use them and they document the model. Ratios such as conversion rate go in a metric view, because an average of averages in a pre-aggregated table is wrong at any other grain.

## Examples

### 1. Materialized view for a pre-computed aggregate

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(name="gold_sales_by_store_day", cluster_by=["order_date"])
def gold_sales_by_store_day():
    f = spark.read.table("main.gold.fact_orders")
    s = spark.read.table("main.gold.dim_store")
    return (f.join(s, "store_sk").groupBy("order_date", "store_sk", "region")
        .agg(F.sum("amount").alias("revenue"), F.countDistinct("order_id").alias("orders")))
```

### 2. Metric view with a governed ratio

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
CREATE OR REPLACE VIEW main.gold.sales_metrics
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
source: main.gold.fact_orders
dimensions:
  - name: order_month
    expr: date_trunc('MONTH', order_date)
measures:
  - name: revenue
    expr: SUM(amount)
  - name: avg_order_value
    expr: SUM(amount) / COUNT(DISTINCT order_id)
$$""")
spark.sql("""
SELECT order_month, MEASURE(revenue), MEASURE(avg_order_value)
FROM main.gold.sales_metrics GROUP BY order_month""").show()
```

## Traps and gotchas

- Measures in a metric view must be read with `MEASURE()`.
- Primary and foreign key constraints in Unity Catalog are informational, not enforced.
- A materialized view is as fresh as its last refresh.
