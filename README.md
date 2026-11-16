# Databricks Field Guide

Every Databricks feature from the first managed Spark runtime to Runtime 19 (November 2026). Each feature folder has a `README.md` (what it is, how it flows, when to choose it, a senior engineer verdict, traps) and at least two runnable PySpark or Python examples (`example_N.py`). Some features also include SQL, YAML (bundles), shell or Terraform examples.

Examples assume a Databricks notebook or job where `spark` and `dbutils` exist, and Unity Catalog names such as `main.silver.orders`. Replace hosts, IDs and endpoint names with your own.

## Folders

- [00-start-here: Start here](00-start-here/README.md)
- [01-lakehouse-core: Lakehouse core](01-lakehouse-core/README.md)
- [02-ingestion: Ingestion](02-ingestion/README.md)
- [03-declarative-pipelines: Lakeflow Spark Declarative Pipelines](03-declarative-pipelines/README.md)
- [04-scd-cdc: SCD and change data](04-scd-cdc/README.md)
- [05-structured-streaming: Structured Streaming](05-structured-streaming/README.md)
- [06-data-manipulation: Data manipulation](06-data-manipulation/README.md)
- [07-orchestration-deploy: Orchestration, testing and deployment](07-orchestration-deploy/README.md)
- [08-performance-cost: Performance and cost](08-performance-cost/README.md)
- [09-governance-security: Governance and security](09-governance-security/README.md)
- [10-monitoring: Monitoring and alerting](10-monitoring/README.md)
- [11-data-modeling: Data modeling](11-data-modeling/README.md)
- [12-spark-engine: Spark engine](12-spark-engine/README.md)
- [13-delta-advanced: Delta and Iceberg features](13-delta-advanced/README.md)
- [14-developer-tools: Developer tools](14-developer-tools/README.md)
- [15-databricks-sql-bi: Databricks SQL and BI](15-databricks-sql-bi/README.md)
- [16-ml-ai: Machine learning and AI](16-ml-ai/README.md)
- [17-apps-lakebase: Apps and Lakebase](17-apps-lakebase/README.md)
- [18-platform-admin: Platform and administration](18-platform-admin/README.md)
- [19-spark4-runtime: Spark 4 and runtime features](19-spark4-runtime/README.md)

## Major features, oldest to newest

| Since | Feature | Area |
|---|---|---|
| 2013 | [How Spark executes your code](12-spark-engine/spark-architecture/README.md) | Spark engine |
| 2013 | [Notebooks, widgets and dbutils](14-developer-tools/notebooks-dbutils/README.md) | Developer tools |
| 2014 | [Databricks Runtime versions from the beginning to 19](19-spark4-runtime/runtime-versions/README.md) | Spark 4 and runtime features |
| 2015 | [Lakeflow Jobs](07-orchestration-deploy/lakeflow-jobs/README.md) | Orchestration, testing and deployment |
| 2015 | [Window functions, joins and aggregations](06-data-manipulation/windows-joins-aggregations/README.md) | Data manipulation |
| 2016 | [REST API, SDKs, CLI and Terraform](14-developer-tools/automation-interfaces/README.md) | Developer tools |
| 2017 | [Delta Lake transaction log](01-lakehouse-core/delta-lake-log/README.md) | Lakehouse core |
| 2017 | [Triggers, checkpoints and exactly-once](05-structured-streaming/streaming-core/README.md) | Structured Streaming |
| 2017 | [Watermarks, state and output modes](05-structured-streaming/streaming-core/watermarks-state/README.md) | Structured Streaming |
| 2018 | [Machine learning lifecycle on Databricks](16-ml-ai/ml-lifecycle/README.md) | Machine learning and AI |
| 2019 | [SCD types and which one to choose](04-scd-cdc/scd-types/README.md) | SCD and change data |
| 2020 | [Accounts, workspaces and identity](18-platform-admin/account-identity/README.md) | Platform and administration |
| 2020 | [Auto Loader](02-ingestion/auto-loader/README.md) | Ingestion |
| 2020 | [Constraints, generated, identity and default columns](13-delta-advanced/table-constraints/README.md) | Delta and Iceberg features |
| 2020 | [Query profile, Spark UI and common bottlenecks](08-performance-cost/query-tuning/README.md) | Performance and cost |
| 2020 | [SQL warehouses](15-databricks-sql-bi/sql-warehouses/README.md) | Databricks SQL and BI |
| 2021 | [AUTO CDC (formerly APPLY CHANGES)](03-declarative-pipelines/sdp-overview/auto-cdc/README.md) | Lakeflow Spark Declarative Pipelines |
| 2021 | [Change Data Feed](04-scd-cdc/change-data-feed/README.md) | SCD and change data |
| 2021 | [Lakeflow Spark Declarative Pipelines (SDP)](03-declarative-pipelines/sdp-overview/README.md) | Lakeflow Spark Declarative Pipelines |
| 2022 | [Model Serving, Foundation Model APIs and AI Gateway](16-ml-ai/model-serving/README.md) | Machine learning and AI |
| 2022 | [Unity Catalog object model and inheritance](09-governance-security/unity-catalog-model/README.md) | Governance and security |
| 2023 | [Data purging and right to erasure](09-governance-security/gdpr-purge/README.md) | Governance and security |
| 2023 | [Declarative Automation Bundles](07-orchestration-deploy/declarative-automation-bundles/README.md) | Orchestration, testing and deployment |
| 2023 | [Iceberg, UniForm and open access](13-delta-advanced/iceberg-uniform/README.md) | Delta and Iceberg features |
| 2023 | [Liquid clustering, partitioning and ZORDER](08-performance-cost/liquid-clustering/README.md) | Performance and cost |
| 2023 | [Predictive optimization, OPTIMIZE and VACUUM](08-performance-cost/predictive-optimization/README.md) | Performance and cost |
| 2023 | [Row filters, column masks and ABAC](09-governance-security/row-filters-masks-abac/README.md) | Governance and security |
| 2023 | [Streaming table or materialized view](03-declarative-pipelines/sdp-overview/streaming-table-vs-mv/README.md) | Lakeflow Spark Declarative Pipelines |
| 2023 | [System tables](10-monitoring/system-tables/README.md) | Monitoring and alerting |
| 2024 | [Agents, Agent Bricks and MLflow 3 evaluation](16-ml-ai/agents-genai/README.md) | Machine learning and AI |
| 2024 | [Databricks Apps](17-apps-lakebase/databricks-apps/README.md) | Apps and Lakebase |
| 2024 | [Lakeflow Connect](02-ingestion/lakeflow-connect/README.md) | Ingestion |
| 2025 | [Dimensional models, materialized views and metric views](11-data-modeling/dimensional-modeling/README.md) | Data modeling |
| 2025 | [Lakebase (managed Postgres)](17-apps-lakebase/lakebase/README.md) | Apps and Lakebase |
| 2025 | [SDP or Structured Streaming](03-declarative-pipelines/sdp-vs-structured-streaming/README.md) | Lakeflow Spark Declarative Pipelines |

## Other features, oldest to newest

| Since | Feature | Area |
|---|---|---|
| 2015 | [Libraries and dependency troubleshooting](07-orchestration-deploy/dependencies/README.md) | Orchestration, testing and deployment |
| 2016 | [Distributed training and Spark ML](16-ml-ai/ml-lifecycle/distributed-ml/README.md) | Machine learning and AI |
| 2016 | [Kafka, Kinesis and Pub/Sub](02-ingestion/message-buses/README.md) | Ingestion |
| 2016 | [Monitoring with REST API, CLI, SDK and streaming metrics](10-monitoring/api-cli-sdk-monitoring/README.md) | Monitoring and alerting |
| 2017 | [Secrets](14-developer-tools/notebooks-dbutils/secrets/README.md) | Developer tools |
| 2017 | [UDFs: Python, pandas and Unity Catalog functions](06-data-manipulation/udfs/README.md) | Data manipulation |
| 2018 | [Arrays, maps, higher-order functions, JSON and XML](19-spark4-runtime/runtime-versions/complex-types-json-xml/README.md) | Spark 4 and runtime features |
| 2018 | [Disk cache, data skipping and Photon](08-performance-cost/disk-cache-photon/README.md) | Performance and cost |
| 2018 | [Stream-static and stream-stream joins](05-structured-streaming/streaming-core/stream-joins/README.md) | Structured Streaming |
| 2019 | [foreachBatch](05-structured-streaming/streaming-core/foreach-batch/README.md) | Structured Streaming |
| 2019 | [MERGE INTO](01-lakehouse-core/merge-into/README.md) | Lakehouse core |
| 2019 | [SCD type 1 with MERGE](04-scd-cdc/scd-types/scd1-merge/README.md) | SCD and change data |
| 2019 | [SCD type 2 with MERGE](04-scd-cdc/scd-types/scd2-merge/README.md) | SCD and change data |
| 2019 | [SCD types 3, 4 and 6](04-scd-cdc/scd-types/scd3-4-6/README.md) | SCD and change data |
| 2019 | [Schema enforcement and evolution](01-lakehouse-core/schema-evolution/README.md) | Lakehouse core |
| 2019 | [Spark Connect and Databricks Connect](12-spark-engine/spark-architecture/databricks-connect/README.md) | Spark engine |
| 2020 | [Alerts and notifications](10-monitoring/alerts/README.md) | Monitoring and alerting |
| 2020 | [COPY INTO](02-ingestion/copy-into/README.md) | Ingestion |
| 2020 | [Deep and shallow clone](01-lakehouse-core/clone/README.md) | Lakehouse core |
| 2020 | [File detection modes](02-ingestion/auto-loader/file-detection-modes/README.md) | Ingestion |
| 2020 | [Git folders and CI/CD](07-orchestration-deploy/git-folders-cicd/README.md) | Orchestration, testing and deployment |
| 2020 | [Medallion architecture](01-lakehouse-core/medallion/README.md) | Lakehouse core |
| 2020 | [Networking and workspace security](18-platform-admin/network-security/README.md) | Platform and administration |
| 2021 | [Expectations (data quality)](03-declarative-pipelines/sdp-overview/expectations/README.md) | Lakeflow Spark Declarative Pipelines |
| 2021 | [Feature engineering and online features](16-ml-ai/ml-lifecycle/feature-engineering/README.md) | Machine learning and AI |
| 2021 | [OpenSharing (Delta Sharing) and Clean Rooms](02-ingestion/sharing-clean-rooms/README.md) | Ingestion |
| 2021 | [pandas API on Spark and pandas functions](12-spark-engine/spark-architecture/pandas-on-spark/README.md) | Spark engine |
| 2021 | [Pipeline event log](10-monitoring/pipeline-event-log/README.md) | Monitoring and alerting |
| 2021 | [Schema inference, evolution and rescued data](02-ingestion/auto-loader/auto-loader-schema/README.md) | Ingestion |
| 2021 | [Triggers, backfills and cleanup](02-ingestion/auto-loader/auto-loader-operations/README.md) | Ingestion |
| 2022 | [Geospatial: H3 and spatial types](19-spark4-runtime/runtime-versions/geospatial/README.md) | Spark 4 and runtime features |
| 2022 | [Least privilege and workspace ACLs](09-governance-security/unity-catalog-model/least-privilege/README.md) | Governance and security |
| 2022 | [Managed and external tables](01-lakehouse-core/managed-vs-external/README.md) | Lakehouse core |
| 2022 | [Pseudonymization, anonymization and PII pipelines](09-governance-security/pii-protection/README.md) | Governance and security |
| 2022 | [Renames, drops and type widening](13-delta-advanced/table-constraints/column-mapping-type-widening/README.md) | Delta and Iceberg features |
| 2022 | [Storage credentials, external locations and volumes](18-platform-admin/account-identity/storage-access/README.md) | Platform and administration |
| 2023 | [AI functions and ai_query](06-data-manipulation/ai-functions/README.md) | Data manipulation |
| 2023 | [Choosing compute](07-orchestration-deploy/compute-choices/README.md) | Orchestration, testing and deployment |
| 2023 | [Data quality monitoring (anomaly detection and profiling)](10-monitoring/data-quality-monitoring/README.md) | Monitoring and alerting |
| 2023 | [Databricks Marketplace](18-platform-admin/marketplace/README.md) | Platform and administration |
| 2023 | [Deletion vectors](08-performance-cost/deletion-vectors/README.md) | Performance and cost |
| 2023 | [Designing Delta and Iceberg table layouts](11-data-modeling/table-layout-design/README.md) | Data modeling |
| 2023 | [Lakehouse Federation](02-ingestion/lakehouse-federation/README.md) | Ingestion |
| 2023 | [Migrating from Hive metastore to Unity Catalog](18-platform-admin/hms-to-uc/README.md) | Platform and administration |
| 2023 | [MLflow tracking and models in Unity Catalog](16-ml-ai/ml-lifecycle/mlflow-uc-models/README.md) | Machine learning and AI |
| 2023 | [Python UDTFs and the Python Data Source API](19-spark4-runtime/runtime-versions/python-udtf-datasource/README.md) | Spark 4 and runtime features |
| 2023 | [Tags, comments and lineage](09-governance-security/tags-comments-lineage/README.md) | Governance and security |
| 2023 | [Unit and integration testing](07-orchestration-deploy/testing/README.md) | Orchestration, testing and deployment |
| 2023 | [Vector Search](16-ml-ai/model-serving/vector-search/README.md) | Machine learning and AI |
| 2024 | [AI/BI dashboards](15-databricks-sql-bi/aibi-dashboards/README.md) | Databricks SQL and BI |
| 2024 | [Append flows and sinks](03-declarative-pipelines/sdp-overview/flows-and-sinks/README.md) | Lakeflow Spark Declarative Pipelines |
| 2024 | [AUTO CDC FROM SNAPSHOT](03-declarative-pipelines/sdp-overview/auto-cdc-from-snapshot/README.md) | Lakeflow Spark Declarative Pipelines |
| 2024 | [Genie (natural-language analytics)](15-databricks-sql-bi/genie/README.md) | Databricks SQL and BI |
| 2024 | [Reading streaming state and checkpoint metadata](19-spark4-runtime/runtime-versions/state-data-source/README.md) | Spark 4 and runtime features |
| 2024 | [VARIANT for semi-structured data](06-data-manipulation/variant/README.md) | Data manipulation |
| 2025 | [Parameterized SQL and SQL scripting](15-databricks-sql-bi/sql-warehouses/sql-scripting-params/README.md) | Databricks SQL and BI |
| 2025 | [Spark 4 SQL: ANSI mode, pipe syntax, collations](19-spark4-runtime/runtime-versions/spark4-sql/README.md) | Spark 4 and runtime features |
| 2025 | [transformWithState and real-time mode](05-structured-streaming/streaming-core/advanced-streaming/README.md) | Structured Streaming |
| 2026 | [New SQL and DataFrame features in Runtime 19](19-spark4-runtime/runtime-versions/runtime-19-functions/README.md) | Spark 4 and runtime features |
| 2026 | [What is new in Runtime 19](00-start-here/runtime-19/README.md) | Start here |

Years are approximate: first preview or general availability on Databricks.
