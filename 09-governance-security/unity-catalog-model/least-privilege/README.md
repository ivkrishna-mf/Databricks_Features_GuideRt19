# Least privilege and workspace ACLs

Available since ~2022 · DE Professional exam: S6 · Part of [Unity Catalog object model and inheritance](../README.md)

## What it is

Give each identity only what its job needs. In Unity Catalog that means narrow grants on data. In the workspace it means permissions on jobs, pipelines, compute, notebooks and secrets.

## How it flows

1. **Identify the role**: Engineer, analyst, service principal.
2. **Data grants**: Read on what they consume, write only on what they produce.
3. **Workspace ACLs**: Can view, can run, can manage on jobs and compute.
4. **Run as**: Production jobs run as a service principal.
5. **Audit**: Check `system.access.audit`.

```
[Identify the role] --> [Data grants] --> [Workspace ACLs] --> [Run as] --> [Audit]
```

## When to choose it

**Choose it when**

- Every production workload.

**Pick something else when**

- ALL PRIVILEGES for convenience.
- Users owning production jobs.

## Senior engineer verdict

> Humans get read in prod and write in dev. Pipelines write as a service principal that has MODIFY only on its own schemas. Secrets live in secret scopes with read ACLs, never in notebooks or job parameters.

## Examples

### 1. Service principal that can write one schema

File: [`example_1.py`](example_1.py)

```python
sp = "`sp-orders-pipeline`"
spark.sql(f"GRANT USE CATALOG ON CATALOG main TO {sp}")
spark.sql(f"GRANT USE SCHEMA, CREATE TABLE, MODIFY, SELECT ON SCHEMA main.silver_orders TO {sp}")
spark.sql(f"GRANT USE SCHEMA, SELECT ON SCHEMA main.bronze_orders TO {sp}")
spark.sql("REVOKE ALL PRIVILEGES ON SCHEMA main.silver_orders FROM `developers`")
```

### 2. Job permissions with the SDK

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import JobAccessControlRequest, JobPermissionLevel
w = WorkspaceClient()
w.jobs.set_permissions(job_id="123", access_control_list=[
    JobAccessControlRequest(group_name="data_engineers", permission_level=JobPermissionLevel.CAN_MANAGE_RUN),
    JobAccessControlRequest(group_name="analysts", permission_level=JobPermissionLevel.CAN_VIEW)])
```

## Traps and gotchas

- MODIFY allows insert, update and delete; it does not include SELECT.
- Can manage run lets a user trigger and cancel runs but not edit the job.
