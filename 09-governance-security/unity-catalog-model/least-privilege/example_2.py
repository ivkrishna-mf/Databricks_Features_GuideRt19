# Job permissions with the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import JobAccessControlRequest, JobPermissionLevel
w = WorkspaceClient()
w.jobs.set_permissions(job_id="123", access_control_list=[
    JobAccessControlRequest(group_name="data_engineers", permission_level=JobPermissionLevel.CAN_MANAGE_RUN),
    JobAccessControlRequest(group_name="analysts", permission_level=JobPermissionLevel.CAN_VIEW)])
