# Classic cluster sized from helpers
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute
w = WorkspaceClient()
cluster = w.clusters.create_and_wait(
    cluster_name="etl-classic",
    spark_version=w.clusters.select_spark_version(latest=True, long_term_support=True),
    node_type_id=w.clusters.select_node_type(local_disk=True, min_memory_gb=32),
    autoscale=compute.AutoScale(min_workers=2, max_workers=8),
    autotermination_minutes=30,
    data_security_mode=compute.DataSecurityMode.USER_ISOLATION)
print(cluster.cluster_id, cluster.spark_version)
