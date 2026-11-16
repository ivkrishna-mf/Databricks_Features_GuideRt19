# Databricks features from the beginning to now

**Major feature**

## What it is

The platform grew in layers. Each layer fixed a pain in the one before it, and knowing the order tells you which feature is the current recommendation and which is legacy. Years are approximate; check the docs when an exact GA date matters.

## How it flows

1. **Managed Spark**: 2013 onward. Notebooks, clusters and jobs around Apache Spark. Problem left open: data lakes had no transactions.
2. **Delta Lake**: 2017 to 2019. ACID log on Parquet, time travel, MERGE. Problem left open: getting files in incrementally and governing them.
3. **Auto Loader, DLT, Photon**: 2020 to 2022. Incremental file ingestion, declarative pipelines, a vectorized engine, Databricks SQL.
4. **Unity Catalog**: 2021 to 2023. One governance layer: catalogs, lineage, sharing, system tables, federation.
5. **Serverless and Lakeflow**: 2024 to 2025. Serverless compute, liquid clustering, predictive optimization, VARIANT, Lakeflow Connect, Pipelines and Jobs.
6. **AI and apps**: 2023 to 2025. MLflow and models in Unity Catalog, Model Serving, Vector Search, Genie, Apps, Lakebase, agents.
7. **Runtime 19 era**: 2026. Declarative Automation Bundles, AUTO CDC, automatic change data feed, ABAC, metric views, Lakebase GA.

```
[Managed Spark] --> [Delta Lake] --> [Auto Loader, DLT, Photon] --> [Unity Catalog] --> [Serverless and Lakeflow] --> [AI and apps] --> [Runtime 19 era]
```

## Timeline

| When | What shipped | Why it matters today |
|---|---|---|
| 2013 | Databricks founded by the creators of Apache Spark; notebooks, clusters, jobs | Still the base: everything runs on Spark |
| 2016 to 2017 | Structured Streaming; Delta announced | Streaming and batch share one DataFrame API |
| 2018 | MLflow open sourced | Experiment tracking and model packaging used across the industry |
| 2019 | Delta Lake open sourced | Transaction log, time travel, schema enforcement |
| 2020 | Auto Loader; lakehouse architecture; Databricks SQL; Photon announced | Incremental file ingestion with `cloudFiles` |
| 2021 | Delta Live Tables, Unity Catalog and Delta Sharing announced | Declarative pipelines and central governance begin |
| 2022 | DLT, Unity Catalog, Photon and Delta Sharing reach GA; multi-task jobs | Medallion pipelines with expectations become standard |
| 2023 | Deletion vectors, liquid clustering preview, predictive optimization, system tables, Lakehouse Federation, UniForm, bundles preview; MosaicML acquired; Model Serving and Vector Search | Low-maintenance tables and the start of Mosaic AI |
| 2024 | Bundles GA, liquid clustering GA, serverless jobs and notebooks, VARIANT, Clean Rooms, Lakeflow announced; AI/BI dashboards and Genie; Databricks Apps preview; Agent Framework | Serverless-first; BI, apps and agents on the same platform |
| 2025 | Lakeflow GA (Connect, Declarative Pipelines, Jobs); DLT renamed; Spark Declarative Pipelines contributed to Apache Spark; AUTO CDC replaces APPLY CHANGES; real-time mode; metric views; ABAC; Lakebase (managed Postgres) and Agent Bricks announced; Apps GA; MLflow 3 | Operational databases and agents join the platform |
| 2026 | Bundles renamed Declarative Automation Bundles (March); Runtime 19 with automatic change data feed; OpenSharing name; Lakebase GA across clouds; data quality monitoring; Genie Agents | What this guide targets |

## Senior engineer verdict

> When two features overlap, the newer one is nearly always the expected answer: liquid clustering over partitioning plus ZORDER, AUTO CDC over hand-written MERGE inside pipelines, file events over directory listing, Unity Catalog over the Hive metastore, serverless over hand-tuned clusters. The older option wins only when the scenario gives a concrete reason.

