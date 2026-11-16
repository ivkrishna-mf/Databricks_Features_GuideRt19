# Create a time series profile and query drift
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import MonitorTimeSeries
w = WorkspaceClient()
w.quality_monitors.create(
    table_name="main.gold.fact_orders",
    assets_dir="/Workspace/Shared/monitors/fact_orders",
    output_schema_name="main.monitoring",
    time_series=MonitorTimeSeries(timestamp_col="order_ts", granularities=["1 day"]))

spark.table("main.monitoring.fact_orders_drift_metrics").where("column_name = 'amount'").show()
