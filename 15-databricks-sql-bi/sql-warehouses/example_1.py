# Create a serverless warehouse with the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType, EndpointTags, EndpointTagPair
w = WorkspaceClient()
wh = w.warehouses.create(
    name="bi-serverless", cluster_size="Small",
    min_num_clusters=1, max_num_clusters=4, auto_stop_mins=10,
    enable_serverless_compute=True,
    warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
    tags=EndpointTags(custom_tags=[EndpointTagPair(key="team", value="bi")])).result()
print(wh.id)
