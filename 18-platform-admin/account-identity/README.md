# Accounts, workspaces and identity

**Major feature** · Available since ~2020

## What it is

An account holds workspaces, Unity Catalog metastores (one per region) and identities. Users, groups and service principals live at the account level, usually synced from your identity provider with SCIM, and are assigned to workspaces. Automation authenticates as a service principal with OAuth (machine to machine) or workload identity federation, not with personal access tokens.

## How it flows

1. **Identity provider**: Users and groups, synced by SCIM.
2. **Account**: Users, groups, service principals, metastores, workspaces.
3. **Workspace assignment**: Groups are given access to workspaces.
4. **Unity Catalog grants**: Privileges on data go to account groups.
5. **Automation**: Service principals with OAuth for jobs and CI.

```
[Identity provider] --> [Account] --> [Workspace assignment] --> [Unity Catalog grants] --> [Automation]
```

## When to choose it

**Choose it when**

- Setting up any team or environment.

**Pick something else when**

- Workspace-local groups (legacy).
- Personal access tokens for production automation.

## Senior engineer verdict

> Every production job runs as a service principal, every grant goes to a group, and groups come from the identity provider. That combination means people can join, move and leave without anyone touching Databricks permissions.

## Examples

### 1. OAuth machine-to-machine authentication for the SDK

File: [`example_1.py`](example_1.py)

```python
# Environment for CI or an external service:
#   DATABRICKS_HOST=https://<workspace>.cloud.databricks.com
#   DATABRICKS_CLIENT_ID=<service principal application id>
#   DATABRICKS_CLIENT_SECRET=<oauth secret>
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()                 # picks up OAuth M2M from the environment
print(w.current_user.me().user_name)
```

### 2. Create a service principal and add it to a group

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import AccountClient
from databricks.sdk.service import iam
a = AccountClient()                   # account host and account id from the profile
sp = a.service_principals.create(display_name="sp-orders-pipeline")
grp = next(a.groups.list(filter='displayName eq "data_pipelines"'))
a.groups.patch(id=grp.id, operations=[iam.Patch(op=iam.PatchOp.ADD, path="members",
                                                value=[{"value": sp.id}])],
               schemas=[iam.PatchSchema.URN_IETF_PARAMS_SCIM_API_MESSAGES_2_0_PATCH_OP])
```

## Traps and gotchas

- One metastore per region; workspaces in that region attach to it.
- Workspace admins are not automatically metastore admins.

## Sub-features

- [Storage credentials, external locations and volumes](storage-access/README.md)
