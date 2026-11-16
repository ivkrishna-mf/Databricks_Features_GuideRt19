# Enable IP access lists with the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.settings import ListType
w = WorkspaceClient()
w.workspace_conf.set_status({"enableIpAccessLists": "true"})
w.ip_access_lists.create(label="corp-vpn", list_type=ListType.ALLOW,
                         ip_addresses=["203.0.113.0/24", "198.51.100.10"])
