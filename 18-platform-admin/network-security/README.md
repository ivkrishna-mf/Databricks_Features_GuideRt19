# Networking and workspace security

Available since ~2020

## What it is

Security controls sit at several layers: private connectivity (Private Link) for front end and back end, IP access lists, serverless egress control with network policies, customer-managed keys for encryption, the compliance security profile for regulated workloads, and audit logs in system tables.

## How it flows

1. **User or client**: Through SSO, from allowed networks.
2. **Front end**: Private Link or IP access lists.
3. **Compute**: Classic in your VPC or VNet; serverless in the Databricks account with network connectivity configs.
4. **Egress**: Network policies restrict outbound destinations.
5. **Data**: Encrypted, optionally with your keys; access audited.

```
[User or client] --> [Front end] --> [Compute] --> [Egress] --> [Data]
```

## When to choose it

**Choose it when**

- Any production or regulated deployment.

**Pick something else when**

- Open public endpoints and unrestricted serverless egress for sensitive data.

## Senior engineer verdict

> Data exfiltration usually happens through egress, not ingress. Restricting serverless egress to approved destinations and keeping storage accessible only from Databricks networks closes most paths.

## Examples

### 1. Enable IP access lists with the SDK

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.settings import ListType
w = WorkspaceClient()
w.workspace_conf.set_status({"enableIpAccessLists": "true"})
w.ip_access_lists.create(label="corp-vpn", list_type=ListType.ALLOW,
                         ip_addresses=["203.0.113.0/24", "198.51.100.10"])
```

### 2. Audit sign-ins and permission changes

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
SELECT event_time, user_identity.email, service_name, action_name, source_ip_address, response.status_code
FROM system.access.audit
WHERE event_date >= current_date() - INTERVAL 7 DAYS
  AND (action_name LIKE '%login%' OR action_name = 'updatePermissions')
ORDER BY event_time DESC""").show(50, truncate=False)
```

## Traps and gotchas

- Enabling an IP access list without your own address in it locks you out of the UI and API.
