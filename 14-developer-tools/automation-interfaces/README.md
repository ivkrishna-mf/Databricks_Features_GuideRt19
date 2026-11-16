# REST API, SDKs, CLI and Terraform

**Major feature** · Available since ~2016

## What it is

Everything in the UI is backed by the REST API. The Databricks SDKs (Python, Java, Go) and the CLI wrap it with authentication, pagination and waiters. Declarative Automation Bundles deploy projects. Terraform manages infrastructure such as workspaces, networking, metastores and account-level identity.

## How it flows

1. **Pick the job**: Ad hoc admin task, application code, project deployment or infrastructure.
2. **Authenticate**: Unified auth: profiles, environment variables, OAuth.
3. **Call**: CLI command, SDK method or declarative config.
4. **Wait and verify**: Waiters for long operations, then check state.

```
[Pick the job] --> [Authenticate] --> [Call] --> [Wait and verify]
```

## When to choose it

**Choose it when**

- Anything you do twice.

**Pick something else when**

- Two tools managing the same resource: Terraform and bundles fighting over a job causes drift.

## Which interface

| Task | Choose |
|---|---|
| One-off admin or scripting from a shell | CLI |
| Logic inside an app, notebook or service | Python SDK |
| Deploy jobs, pipelines, dashboards of a project | Declarative Automation Bundles |
| Workspaces, networking, metastore, account groups | Terraform provider |
| Something no wrapper covers yet | REST API (or `w.api_client.do`) |

## Senior engineer verdict

> My split: Terraform owns the platform (workspaces, network, catalogs, groups), bundles own the data products (jobs, pipelines, dashboards), and the SDK is for glue code and operations. One owner per resource, always.

## Examples

### 1. Python SDK: create a job and run it

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
w = WorkspaceClient()        # reads profile or env vars

job = w.jobs.create(name="adhoc-backfill", tasks=[
    jobs.Task(task_key="main",
              notebook_task=jobs.NotebookTask(notebook_path="/Workspace/Shared/backfill",
                                              base_parameters={"start": "2026-01-01"}))])
run = w.jobs.run_now(job_id=job.job_id).result()      # waits until done
print(run.state.result_state)
```

### 2. Raw REST call through the SDK client

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
resp = w.api_client.do("GET", "/api/2.2/jobs/list", query={"limit": 5, "expand_tasks": "false"})
for j in resp.get("jobs", []):
    print(j["job_id"], j["settings"]["name"])
```

### 3. Terraform: catalog, schema and grants

File: [`example_3.tf`](example_3.tf)

```hcl
resource "databricks_catalog" "sales" {
  name    = "sales"
  comment = "Sales domain"
}

resource "databricks_schema" "gold" {
  catalog_name = databricks_catalog.sales.name
  name         = "gold"
}

resource "databricks_grants" "gold" {
  schema = "${databricks_catalog.sales.name}.${databricks_schema.gold.name}"
  grant {
    principal  = "analysts"
    privileges = ["USE_SCHEMA", "SELECT"]
  }
}
```

## Traps and gotchas

- The SDK, CLI and Terraform share unified authentication: the same profile works everywhere.
- Account-level APIs (identity, workspaces) use the account host, not a workspace URL.
