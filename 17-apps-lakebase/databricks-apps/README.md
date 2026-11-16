# Databricks Apps

**Major feature** · Available since ~2024

## What it is

Databricks Apps host web applications (Streamlit, Dash, Gradio, Flask, FastAPI, Node.js) on serverless compute inside the workspace. Each app gets its own service principal, single sign-on for users, and declared resources such as a SQL warehouse, serving endpoint, Lakebase database, secret or Genie space, so the app never handles raw credentials.

## How it flows

1. **Code and app.yaml**: Command to start the app and environment variables.
2. **Resources**: Warehouse, endpoint, database, secrets, granted to the app.
3. **Deploy**: From the UI, CLI or a bundle.
4. **Users sign in**: Workspace SSO; access controlled by app permissions.
5. **Calls**: As the app service principal, or on behalf of the user.

```
[Code and app.yaml] --> [Resources] --> [Deploy] --> [Users sign in] --> [Calls]
```

## When to choose it

**Choose it when**

- Internal tools, data entry, model or agent front ends that need governed data.
- You want hosting, auth and networking handled for you.

**Pick something else when**

- Public internet consumer apps with high traffic.

## Senior engineer verdict

> Decide early whose identity each call uses. App authorization (the service principal) is simple and shared; user authorization (on behalf of the user) means Unity Catalog permissions follow each person. For anything with row-level security I use user authorization.

## Examples

### 1. FastAPI app calling a serving endpoint on behalf of the user

File: [`example_1.py`](example_1.py)

```python
from fastapi import FastAPI, Request
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config

app = FastAPI()

@app.post("/score")
async def score(request: Request, payload: dict):
    user_token = request.headers.get("x-forwarded-access-token")     # user authorization
    w = WorkspaceClient(config=Config(host=Config().host, token=user_token)) if user_token else WorkspaceClient()
    resp = w.serving_endpoints.query(name="churn-scoring", dataframe_records=[payload])
    return {"prediction": resp.predictions[0]}
```

### 2. app.yaml with resources

File: [`example_2.yml`](example_2.yml)

```yaml
command: ["streamlit", "run", "app.py"]
env:
  - name: WAREHOUSE_ID
    valueFrom: sql-warehouse          # resource key declared for the app
  - name: SERVING_ENDPOINT
    valueFrom: serving-endpoint
```

### 3. Streamlit app querying a warehouse

File: [`example_3.py`](example_3.py)

```python
import os
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

cfg = Config()     # app service principal credentials are injected
conn = sql.connect(server_hostname=cfg.host,
                   http_path=f"/sql/1.0/warehouses/{os.environ['WAREHOUSE_ID']}",
                   credentials_provider=lambda: cfg.authenticate)
region = st.selectbox("Region", ["EMEA", "AMER", "APAC"])
with conn.cursor() as cur:
    cur.execute("SELECT order_date, SUM(amount) AS revenue FROM main.gold.fact_orders "
                "WHERE region = :r GROUP BY order_date ORDER BY order_date", {"r": region})
    st.line_chart(cur.fetchall_arrow().to_pandas(), x="order_date", y="revenue")
```

## Traps and gotchas

- Grant the app's service principal access to the tables and resources it uses.
- Apps listen on the port given in `DATABRICKS_APP_PORT`; frameworks configured by Databricks handle this.
