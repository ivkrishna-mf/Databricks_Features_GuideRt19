# OAuth machine-to-machine authentication for the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Environment for CI or an external service:
#   DATABRICKS_HOST=https://<workspace>.cloud.databricks.com
#   DATABRICKS_CLIENT_ID=<service principal application id>
#   DATABRICKS_CLIENT_SECRET=<oauth secret>
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()                 # picks up OAuth M2M from the environment
print(w.current_user.me().user_name)
