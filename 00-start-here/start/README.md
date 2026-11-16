# How this guide is organized

**Major feature**

## What it is

This is a field guide to the whole Databricks platform, organized like a repository: each folder is a major area, each page a feature, and sub-pages sit under the feature they extend. Every page has the same parts: what it is, an animated flow you can step through, when to choose it and when not to, a senior engineer's verdict, two or more runnable examples, and the traps that catch people.

Read the major pages in a folder first, then the sub-pages. Examples use Python (PySpark) unless SQL, YAML or shell is the natural tool, and assume Unity Catalog names such as `main.silver.orders`. Mark pages as studied to track progress in this browser.

Several products were renamed recently. Delta Live Tables is now Lakeflow Spark Declarative Pipelines, APPLY CHANGES is AUTO CDC, Databricks Asset Bundles are Declarative Automation Bundles, Repos are Git folders, Delta Sharing appears as OpenSharing, Lakehouse Monitoring is data profiling, and Genie spaces are Genie Agents.

## Folders

| Folder | Covers |
|---|---|
| 01 Lakehouse core | Delta log, medallion, managed tables, schema evolution, MERGE, clone |
| 02 Ingestion | Auto Loader, COPY INTO, message buses, Lakeflow Connect, federation, sharing |
| 03 Declarative pipelines | SDP, streaming tables and materialized views, expectations, AUTO CDC, flows |
| 04 SCD and change data | SCD types 0 to 6, MERGE patterns, change data feed |
| 05 Structured Streaming | Triggers, checkpoints, watermarks, joins, foreachBatch, transformWithState |
| 06 Data manipulation | Windows and joins, VARIANT, AI functions, UDFs |
| 07 Orchestration and deployment | Jobs, compute, bundles, Git and CI/CD, testing, dependencies |
| 08 Performance and cost | Liquid clustering, deletion vectors, predictive optimization, caching, tuning |
| 09 Governance and security | Unity Catalog, privileges, ABAC, PII, erasure, tags and lineage |
| 10 Monitoring | System tables, event logs, alerts, APIs, data quality monitoring |
| 11 Data modeling | Table layout, dimensional models, metric views |
| 12 Spark engine | Execution model, Databricks Connect, pandas on Spark |
| 13 Delta and Iceberg features | Constraints, identity columns, renames, Iceberg and UniForm |
| 14 Developer tools | Notebooks and dbutils, secrets, SDK, CLI, Terraform |
| 15 Databricks SQL and BI | Warehouses, parameterized SQL and scripting, dashboards, Genie |
| 16 Machine learning and AI | MLflow, models in UC, features, serving, AI Gateway, vector search, agents |
| 17 Apps and Lakebase | Databricks Apps, managed Postgres and synced tables |
| 18 Platform and administration | Identity, storage access, networking, Hive metastore migration, Marketplace |

## Senior engineer verdict

> Learn the platform in the order data flows: land it (ingestion), shape it (pipelines, streaming, SCD), make it fast and cheap (performance), govern it, then serve it (SQL, BI, ML, apps). Run each example in a workspace; the Free Edition is enough for most of them.

