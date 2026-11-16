# Manage scopes and ACLs with the Python SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import AclPermission
w = WorkspaceClient()
w.secrets.create_scope(scope="crm")
w.secrets.put_secret(scope="crm", key="api_key", string_value=os.environ["CRM_API_KEY"])
w.secrets.put_acl(scope="crm", principal="sp-orders-pipeline", permission=AclPermission.READ)
print([s.key for s in w.secrets.list_secrets(scope="crm")])
