# OpenSharing (Delta Sharing) and Clean Rooms

Available since ~2021 · DE Professional exam: S2

## What it is

Sharing gives another party live, read-only access to tables, views and volumes with no copy. Databricks-to-Databricks sharing links two Unity Catalog metastores by a sharing identifier. Open sharing gives any client a credential (token or OIDC) to read with a connector.

Clean Rooms let several parties run approved notebooks over combined data without anyone seeing the raw tables of the others.

## How it flows

1. **Provider creates a share**: A securable that lists tables, views, volumes.
2. **Recipient**: Databricks-to-Databricks uses a metastore identifier; open sharing issues a credential.
3. **GRANT SELECT ON SHARE**: Recipient gets access.
4. **Recipient reads**: As a catalog (D2D) or through a sharing client (open). Data stays in provider storage.

```
[Provider creates a share] --> [Recipient] --> [GRANT SELECT ON SHARE] --> [Recipient reads]
```

## When to choose it

**Choose it when**

- Cross-organization or cross-region data exchange.
- Joint analysis on sensitive data: Clean Rooms.

**Pick something else when**

- Recipients need to write back: sharing is read-only.
- Same-metastore access: plain grants are enough.

## Senior engineer verdict

> D2D when the other side has Unity Catalog, because there are no tokens to rotate and lineage and audit carry through. Open sharing for everyone else. Share with history only when the recipient needs time travel, streaming or the change feed.

## Examples

### 1. Provider: share a table with history

File: [`example_1.py`](example_1.py)

```python
spark.sql("CREATE SHARE IF NOT EXISTS retail_share")
spark.sql("ALTER SHARE retail_share ADD TABLE main.gold.daily_sales WITH HISTORY")
spark.sql("CREATE RECIPIENT partner_co USING ID 'aws:us-west-2:19a8...'")   # D2D identifier
spark.sql("GRANT SELECT ON SHARE retail_share TO RECIPIENT partner_co")
```

### 2. Recipient: mount and stream the share

File: [`example_2.py`](example_2.py)

```python
spark.sql("CREATE CATALOG partner_retail USING SHARE acme.retail_share")
stream = (spark.readStream
    .option("readChangeFeed", "true")
    .table("partner_retail.gold.daily_sales"))
```

## Traps and gotchas

- Open recipients authenticate with a credential file; D2D recipients do not use tokens.
- Streaming or CDF on a shared table requires that it was shared WITH HISTORY.
