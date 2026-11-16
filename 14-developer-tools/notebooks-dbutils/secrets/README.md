# Secrets

Available since ~2017 · Part of [Notebooks, widgets and dbutils](../README.md)

## What it is

Secret scopes store credentials such as API keys and database passwords. Code reads them at runtime with `dbutils.secrets.get` or the SQL `secret()` function, and their values are redacted in notebook output. Access is controlled with ACLs on each scope.

## How it flows

1. **Admin creates scope**: Databricks-backed or backed by a cloud key vault.
2. **Put secret**: With the CLI or API.
3. **Grant READ**: To the group or service principal that needs it.
4. **Read at runtime**: Value is used, never printed.

```
[Admin creates scope] --> [Put secret] --> [Grant READ] --> [Read at runtime]
```

## When to choose it

**Choose it when**

- Any credential used by code or connections.

**Pick something else when**

- Hard-coding credentials in notebooks, job parameters or bundle files.
- Secrets for Databricks-to-Databricks auth: use OAuth service principals instead.

## Senior engineer verdict

> Prefer identities to secrets: Unity Catalog storage credentials, service credentials and connections remove most of the secrets people used to need. What is left goes in one scope per application with READ granted to its service principal only.

## Examples

### 1. Manage scopes and ACLs with the Python SDK

File: [`example_1.py`](example_1.py)

```python
import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import AclPermission
w = WorkspaceClient()
w.secrets.create_scope(scope="crm")
w.secrets.put_secret(scope="crm", key="api_key", string_value=os.environ["CRM_API_KEY"])
w.secrets.put_acl(scope="crm", principal="sp-orders-pipeline", permission=AclPermission.READ)
print([s.key for s in w.secrets.list_secrets(scope="crm")])
```

### 2. Create a scope and grant access with the CLI

File: [`example_2.sh`](example_2.sh)

```bash
databricks secrets create-scope crm
databricks secrets put-secret crm api_key --string-value "$CRM_API_KEY"
databricks secrets put-acl crm sp-orders-pipeline READ
databricks secrets list-secrets crm
```

### 3. Read secrets in Python and SQL

File: [`example_3.py`](example_3.py)

```python
import requests
key = dbutils.secrets.get(scope="crm", key="api_key")
r = requests.get("https://api.crm.example/v1/accounts", headers={"Authorization": "Bearer " + key}, timeout=30)
print(key)      # prints [REDACTED]

spark.sql("SELECT secret('crm', 'api_key') IS NOT NULL AS has_key").show()
```

## Traps and gotchas

- Redaction only hides the literal value in output; transforming it (for example reversing it) can leak it. Treat code with secret access as sensitive.
- Secret scope ACLs are MANAGE, WRITE and READ.
