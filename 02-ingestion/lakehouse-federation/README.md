# Lakehouse Federation

Available since ~2023 · DE Professional exam: S2

## What it is

Query external systems such as PostgreSQL, SQL Server, Snowflake, BigQuery or Redshift in place. A connection stores how to reach the system, and a foreign catalog exposes its schemas in Unity Catalog. Filters and aggregates are pushed down where possible.

## How it flows

1. **CREATE CONNECTION**: Host, port and a credential for the remote system.
2. **CREATE FOREIGN CATALOG**: Mirrors the remote database as a read-only catalog.
3. **Grant in UC**: Users need privileges on the foreign catalog; they never see the credential.
4. **Query**: Spark pushes predicates down and reads the result.

```
[CREATE CONNECTION] --> [CREATE FOREIGN CATALOG] --> [Grant in UC] --> [Query]
```

## When to choose it

**Choose it when**

- Proofs of concept, ad hoc analysis, or a gradual migration.
- Data that cannot be copied for policy reasons.

**Pick something else when**

- High-volume or frequent pipelines. Load on the source and latency make ingestion the better choice.

## Senior engineer verdict

> Federation is governance plus convenience. Two layers of security apply: the connection credential decides what the remote system allows, and Unity Catalog decides which Databricks users may use it. Every user shares the connection identity unless you configure per-user credentials.

## Examples

### 1. Connection and foreign catalog

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE CONNECTION pg_crm TYPE postgresql
OPTIONS (host 'crm.acme.internal', port '5432',
         user secret('crm', 'user'), password secret('crm', 'pwd'))""")
spark.sql("CREATE FOREIGN CATALOG crm USING CONNECTION pg_crm OPTIONS (database 'crm')")
spark.sql("GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG crm TO `analysts`")
```

### 2. Join federated and lakehouse data

File: [`example_2.py`](example_2.py)

```python
accounts = spark.table("crm.public.accounts").where("region = 'EMEA'")   # pushed down
orders = spark.table("main.gold.fact_orders")
orders.join(accounts, "account_id").groupBy("segment").sum("amount").show()
```

## Traps and gotchas

- Foreign catalogs are read-only.
- Privileges on the foreign catalog are needed in addition to what the connection user can do remotely.
