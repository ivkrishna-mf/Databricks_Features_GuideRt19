# Publish and list dashboards with the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
d = next(x for x in w.lakeview.list() if x.display_name == "Sales overview")
w.lakeview.publish(dashboard_id=d.dashboard_id, warehouse_id="<warehouse-id>", embed_credentials=True)
print(d.dashboard_id, d.lifecycle_state)
