# Iceberg, UniForm and open access

**Major feature** · Available since ~2023

## What it is

Unity Catalog stores tables as Delta or Apache Iceberg. Managed Iceberg tables are first-class: predictive optimization, liquid clustering and governance apply. UniForm writes Iceberg metadata for a Delta table so Iceberg readers see the same files. External engines (Spark, Trino, Snowflake, DuckDB) read and write through the Unity Catalog Iceberg REST catalog with credential vending.

## How it flows

1. **Table in UC**: Managed Delta or managed Iceberg.
2. **Metadata**: Delta log, Iceberg metadata, or both with UniForm.
3. **REST catalog**: External engines discover tables through Unity Catalog.
4. **Credential vending**: UC gives short-lived storage credentials scoped to the table.
5. **Governance**: Same grants apply in and outside Databricks.

```
[Table in UC] --> [Metadata] --> [REST catalog] --> [Credential vending] --> [Governance]
```

## When to choose it

**Choose it when**

- Multi-engine architectures where you want one copy of the data.

**Pick something else when**

- Copying data into a second format with a nightly job.

## Choosing a format

| Need | Choose |
|---|---|
| Databricks-centric workloads | Managed Delta |
| Other engines must read the same table | Managed Delta with UniForm, or managed Iceberg |
| Other engines must also write | Managed Iceberg through the Iceberg REST catalog |
| Tables already managed by an external Iceberg catalog | Catalog federation, query them in place |

## Senior engineer verdict

> Format wars are over in practice: pick Delta for Databricks-heavy work, flip on UniForm when someone else needs to read it, and choose managed Iceberg when another engine must write. The governance layer is the part that matters, and it is the same either way.

## Examples

### 1. Managed Iceberg table and a UniForm Delta table

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE TABLE main.gold.orders_ice (order_id BIGINT, amount DECIMAL(18,2), order_date DATE)
USING ICEBERG CLUSTER BY (order_date)""")

spark.sql("""
ALTER TABLE main.gold.fact_orders SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg')""")
```

### 2. External Spark reading through the Unity Catalog Iceberg REST catalog

File: [`example_2.py`](example_2.py)

```python
# Runs outside Databricks (open-source Spark with the Iceberg runtime jar)
from pyspark.sql import SparkSession
spark = (SparkSession.builder
    .config("spark.sql.catalog.uc", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.uc.type", "rest")
    .config("spark.sql.catalog.uc.uri", "https://<workspace-host>/api/2.1/unity-catalog/iceberg-rest")
    .config("spark.sql.catalog.uc.warehouse", "main")
    .config("spark.sql.catalog.uc.token", "<oauth-token>")
    .getOrCreate())
spark.table("uc.gold.orders_ice").show()
```

## Traps and gotchas

- UniForm needs column mapping and disables deletion vectors on older protocol versions; check the requirements before enabling.
- External access requires the EXTERNAL USE SCHEMA privilege in addition to SELECT.
