# Databricks Marketplace

Available since ~2023

## What it is

An open marketplace for datasets, notebooks, models and solution accelerators, delivered through sharing. Consumers install a listing and get a read-only catalog with no copy. Providers publish shares as free, private or paid listings.

## How it flows

1. **Provider**: Creates a share and a listing.
2. **Consumer finds listing**: Browse or private exchange.
3. **Install**: Creates a catalog from the share.
4. **Query**: Like any Unity Catalog data, governed by grants.

```
[Provider] --> [Consumer finds listing] --> [Install] --> [Query]
```

## When to choose it

**Choose it when**

- You need third-party reference data (weather, demographics, firmographics) without building ingestion.

**Pick something else when**

- Data that must be modified in place: copy it into your own tables.

## Senior engineer verdict

> Installed listings are shares, so the provider controls freshness and schema. I wrap them with a view in my own schema, so a provider change breaks one view instead of every downstream job.

## Examples

### 1. Use an installed listing

File: [`example_1.py`](example_1.py)

```python
spark.sql("SHOW SCHEMAS IN acme_weather_data").show()
spark.sql("GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG acme_weather_data TO `analysts`")
spark.sql("""
CREATE OR REPLACE VIEW main.ref.daily_weather AS
SELECT station_id, obs_date, avg_temp_c FROM acme_weather_data.public.daily_obs""")
```

### 2. Provider side: prepare a share for a listing

File: [`example_2.py`](example_2.py)

```python
spark.sql("CREATE SHARE IF NOT EXISTS public_reference COMMENT 'Listing: retail calendar'")
spark.sql("ALTER SHARE public_reference ADD TABLE main.ref.retail_calendar")
# Then create the listing in the Marketplace provider console and attach the share
```

## Traps and gotchas

- Marketplace data is read-only to the consumer.
