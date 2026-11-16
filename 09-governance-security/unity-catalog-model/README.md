# Unity Catalog object model and inheritance

**Major feature** · Available since ~2022 · DE Professional exam: S6, S7

## What it is

Unity Catalog is the governance layer. Securable objects form a hierarchy: metastore, catalog, schema, then tables, views, volumes, functions and models. Privileges granted on a parent are inherited by current and future children.

## How it flows

1. **Metastore**: One per region, attached to workspaces.
2. **Catalog**: Top-level container, often per environment or domain.
3. **Schema**: Groups related objects.
4. **Table, view, volume, function**: The data and code objects.
5. **Query**: Needs USE CATALOG, USE SCHEMA and the object privilege.

```
[Metastore] --> [Catalog] --> [Schema] --> [Table, view, volume, function] --> [Query]
```

## When to choose it

**Choose it when**

- Always for new work. It is required for serverless, lineage, sharing, ABAC and predictive optimization.

**Pick something else when**

- Granting to individual users. Grant to groups.

## Senior engineer verdict

> I design catalogs around ownership boundaries (environment or domain), grant at the schema level to groups, and make groups or service principals the owners. Inheritance means one grant at the right level replaces hundreds of table grants.

## Examples

### 1. Grants that inherit

File: [`example_1.py`](example_1.py)

```python
spark.sql("GRANT USE CATALOG ON CATALOG main TO `data_analysts`")
spark.sql("GRANT USE SCHEMA, SELECT ON SCHEMA main.gold TO `data_analysts`")   # all current and future tables
spark.sql("SHOW GRANTS ON SCHEMA main.gold").show(truncate=False)
```

### 2. Three-level names and volumes

File: [`example_2.py`](example_2.py)

```python
df = spark.table("main.gold.daily_revenue")
spark.sql("CREATE VOLUME IF NOT EXISTS main.landing.orders")
files = dbutils.fs.ls("/Volumes/main/landing/orders/")
spark.sql("ALTER SCHEMA main.gold OWNER TO `gold_owners`")
```

## Traps and gotchas

- SELECT on a table is not enough: the user also needs USE CATALOG and USE SCHEMA on its parents.
- A grant on a catalog applies to schemas and tables created later.
- Owners have all privileges on the object and can grant them; MANAGE delegates that without changing the owner.

## Sub-features

- [Least privilege and workspace ACLs](least-privilege/README.md)
