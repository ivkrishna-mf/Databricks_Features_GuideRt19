# Raw REST call through the SDK client
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
resp = w.api_client.do("GET", "/api/2.2/jobs/list", query={"limit": 5, "expand_tasks": "false"})
for j in resp.get("jobs", []):
    print(j["job_id"], j["settings"]["name"])
