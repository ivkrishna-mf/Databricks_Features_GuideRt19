# Databricks Runtime versions from the beginning to 19

**Major feature** · Available since ~2014

## What it is

A Databricks Runtime bundles Apache Spark with Delta Lake, Photon, libraries and Databricks-only features. Long-term support (LTS) versions get about three years of fixes and are what most production jobs pin. Serverless compute tracks recent runtimes automatically, so you choose an environment version instead of a runtime.

## How it flows

1. **Pick a version**: LTS for classic production jobs, latest for new features, serverless to stop choosing.
2. **Read release notes**: Behavior changes matter more than new features.
3. **Test**: Run the test suite on the new version.
4. **Pin**: Set spark_version in the bundle, or the serverless environment version.
5. **Upgrade on schedule**: Move before end of support.

```
[Pick a version] --> [Read release notes] --> [Test] --> [Pin] --> [Upgrade on schedule]
```

## When to choose it

**Choose it when**

- Choosing or upgrading the runtime for classic compute.

**Pick something else when**

- Running production on a non-LTS runtime without a plan to upgrade within months.

## Milestones by runtime (Spark version in brackets)

| Runtime | Year | Headline features |
|---|---|---|
| 1.x to 3.x (Spark 1.x to 2.x) | 2014 to 2017 | Managed Spark, notebooks, jobs, DataFrames, Structured Streaming |
| 4.x to 6.x (Spark 2.3 to 2.4) | 2018 to 2019 | Databricks Delta, Delta cache, pandas UDFs, Delta Lake open sourced |
| 7.3 LTS (Spark 3.0) | 2020 | Adaptive Query Execution, dynamic partition pruning, Auto Loader, COPY INTO |
| 9.1 LTS (Spark 3.1) | 2021 | Faster directory listing for Auto Loader, Photon on clusters |
| 10.4 LTS (Spark 3.2) | 2022 | pandas API on Spark, Trigger.AvailableNow, Delta change data feed matured |
| 11.3 LTS (Spark 3.3) | 2022 | Unity Catalog GA, column mapping drops and renames, Python 3.9 |
| 12.2 LTS (Spark 3.3) | 2023 | Schema evolution in MERGE improvements, Kinesis and Pub/Sub sources |
| 13.3 LTS (Spark 3.4) | 2023 | Spark Connect, Databricks Connect v2, shared access mode with Python UDFs, volumes |
| 14.3 LTS (Spark 3.5) | 2024 | Deletion vectors widely on, liquid clustering, pyspark.testing, native XML, state reader |
| 15.4 LTS (Spark 3.5) | 2024 | VARIANT type, Python UDTFs in UC, row filters and masks on more compute |
| 16.4 LTS (Spark 3.5) | 2025 | Liquid clustering by default patterns, SQL scripting preview, collations |
| 17.3 LTS (Spark 4.0) | 2025 | ANSI SQL mode by default, SQL pipe syntax, Python data source API, real-time mode preview |
| 18 (Spark 4.x) | 2026 | transformWithState GA, spatial types, more managed Iceberg features |
| 19 (Spark 4.x) | 2026 | Automatic change data feed, INSERT REPLACE ON/USING, withSchemaEvolution, SET PATH, Arrow UDFs by default, Java 21 only |

## Senior engineer verdict

> I keep production on the latest LTS or serverless, test the next one in CI, and read the behavior changes section of every release note before upgrading. The features rarely break anything; the defaults that changed do (ANSI mode in Spark 4 was the big one).

## Examples

### 1. Check the runtime and Spark version from code

File: [`example_1.py`](example_1.py)

```python
import os
print(spark.version)                                               # Apache Spark version
print(os.environ.get("DATABRICKS_RUNTIME_VERSION"))                # e.g. "19.0"
print(spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion", "serverless"))
```

### 2. Guard a feature by runtime version

File: [`example_2.py`](example_2.py)

```python
import os
major = int(os.environ.get("DATABRICKS_RUNTIME_VERSION", "0").split(".")[0] or 0)
if major >= 19:
    changes = spark.read.option("readChangeFeed", "true").option("startingVersion", 10).table("main.silver.orders")
else:
    spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
    changes = spark.read.option("readChangeFeed", "true").option("startingVersion", 10).table("main.silver.orders")
```

## Traps and gotchas

- Serverless ignores the runtime you pick on a cluster; it uses its own environment versions.
- ANSI mode (Spark 4) turns silent nulls from bad casts or overflows into errors.

## Sub-features

- [Spark 4 SQL: ANSI mode, pipe syntax, collations](spark4-sql/README.md)
- [Python UDTFs and the Python Data Source API](python-udtf-datasource/README.md)
- [Arrays, maps, higher-order functions, JSON and XML](complex-types-json-xml/README.md)
- [Geospatial: H3 and spatial types](geospatial/README.md)
- [Reading streaming state and checkpoint metadata](state-data-source/README.md)
- [New SQL and DataFrame features in Runtime 19](runtime-19-functions/README.md)
