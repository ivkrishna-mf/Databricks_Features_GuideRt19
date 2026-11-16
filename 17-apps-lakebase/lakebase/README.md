# Lakebase (managed Postgres)

**Major feature** · Available since ~2025

## What it is

Lakebase is serverless Postgres inside the platform for operational workloads: app state, transactions, low-latency lookups and agent memory. It separates compute from storage, autoscales and scales to zero, and supports instant branching for dev and test copies. Synced tables copy Unity Catalog tables into Postgres for fast reads, and Lakehouse Sync (preview) replicates Postgres tables back into the lakehouse.

## How it flows

1. **Lakehouse tables**: Gold data in Unity Catalog.
2. **Synced table**: Managed pipeline copies rows into a read-only Postgres table.
3. **App writes**: Operational tables in the same database, full ACID.
4. **Branch**: Copy-on-write database branches for testing.
5. **Back to lakehouse**: Lakehouse Sync or a database catalog for analytics.

```
[Lakehouse tables] --> [Synced table] --> [App writes] --> [Branch] --> [Back to lakehouse]
```

## When to choose it

**Choose it when**

- Applications and agents that need a transactional database next to their analytics data.

**Pick something else when**

- Analytical scans over billions of rows: that is what the lakehouse is for.

## Lakebase or Delta

| Workload | Choose |
|---|---|
| Many small reads and writes by key, transactions, millisecond latency | Lakebase |
| Scans, aggregations, large batch or streaming ETL | Delta tables |
| Serve gold data to an app | Synced table from Delta to Lakebase |
| Analyze app data | Sync back to Unity Catalog or query through a catalog |

## Senior engineer verdict

> Lakebase removed the reverse-ETL pipeline I used to build for every app: gold table to Redis or RDS with a custom job. Now it is a synced table. I keep synced tables read-only, put writable app state in separate tables, and use branches for schema migrations.

## Examples

### 1. Connect from a Databricks App with OAuth

File: [`example_1.py`](example_1.py)

```python
import os
import psycopg
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
token = w.config.oauth_token().access_token        # short-lived, used as the password
with psycopg.connect(host=os.environ["PGHOST"], dbname=os.environ.get("PGDATABASE", "databricks_postgres"),
                     user=os.environ["PGUSER"], password=token, sslmode="require") as conn:
    cur = conn.execute("SELECT segment, lifetime_value FROM serving.customer_profile WHERE customer_id = %s",
                       ("C-1042",))
    print(cur.fetchone())
    conn.execute("INSERT INTO app.feedback (customer_id, note) VALUES (%s, %s)", ("C-1042", "called back"))
```

### 2. Read a Lakebase table into Spark over JDBC

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
token = WorkspaceClient().config.oauth_token().access_token
feedback = (spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://<lakebase-host>:5432/databricks_postgres?sslmode=require")
    .option("dbtable", "app.feedback")
    .option("user", "<your-user-or-service-principal>")
    .option("password", token)
    .load())
feedback.write.mode("overwrite").saveAsTable("main.bronze.app_feedback")
```

### 3. Define a database and catalog in a bundle

File: [`example_3.yml`](example_3.yml)

```yaml
resources:
  database_instances:
    app_db:
      name: app-db
      capacity: CU_1
  database_catalogs:
    app_catalog:
      database_instance_name: ${resources.database_instances.app_db.name}
      name: app_catalog
      database_name: databricks_postgres
      create_database_if_not_exists: true
```

## Traps and gotchas

- Synced tables are read-only in Postgres; write to separate tables.
- Complex types (ARRAY, MAP, STRUCT) land in Postgres as JSONB.
- OAuth tokens expire; refresh them in long-running apps.
