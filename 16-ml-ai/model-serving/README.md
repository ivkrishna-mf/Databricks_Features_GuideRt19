# Model Serving, Foundation Model APIs and AI Gateway

**Major feature** · Available since ~2022

## What it is

Model Serving hosts models behind a REST endpoint that scales automatically, including to zero. It serves your MLflow models, foundation models through pay-per-token or provisioned throughput, and external models such as OpenAI or Anthropic through one interface. AI Gateway adds governance on any endpoint: permissions, rate limits, usage tracking, guardrails and inference tables that log requests and responses to Delta.

## How it flows

1. **Client request**: REST, SDK, OpenAI-compatible client or ai_query.
2. **AI Gateway**: Auth, rate limits, guardrails, fallbacks.
3. **Served entity**: Custom model, foundation model or external model.
4. **Response**: Returned to the caller.
5. **Inference table**: Request and response logged for monitoring and evaluation.

```
[Client request] --> [AI Gateway] --> [Served entity] --> [Response] --> [Inference table]
```

## When to choose it

**Choose it when**

- Predictions or generations needed at request time.
- Central control of which LLMs teams use and how much.

**Pick something else when**

- Scoring large tables row by row through an endpoint from a loop: use batch inference or ai_query.

## Senior engineer verdict

> I put every LLM call behind a Databricks endpoint with AI Gateway, even external providers. Keys stay in one place, usage is attributable, and switching models is a config change. Inference tables are the cheapest monitoring you will ever get; turn them on from day one.

## Examples

### 1. Create an endpoint for a UC model

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointCoreConfigInput, ServedEntityInput
w = WorkspaceClient()
w.serving_endpoints.create_and_wait(
    name="churn-scoring",
    config=EndpointCoreConfigInput(served_entities=[
        ServedEntityInput(entity_name="main.ml.churn_model", entity_version="7",
                          workload_size="Small", scale_to_zero_enabled=True)]))
resp = w.serving_endpoints.query(name="churn-scoring",
                                 dataframe_records=[{"tenure": 14, "monthly_spend": 42.0}])
print(resp.predictions)
```

### 2. Call a foundation model with the OpenAI client

File: [`example_2.py`](example_2.py)

```python
from databricks.sdk import WorkspaceClient
client = WorkspaceClient().serving_endpoints.get_open_ai_client()
out = client.chat.completions.create(
    model="databricks-claude-sonnet-4",          # any chat endpoint name in your workspace
    messages=[{"role": "user", "content": "Summarize this ticket in one sentence: ..."}],
    max_tokens=100)
print(out.choices[0].message.content)
```

## Traps and gotchas

- Scale to zero saves cost but adds a cold start on the first request.
- Endpoint names available differ by workspace and region; list them before hard-coding one.

## Sub-features

- [Vector Search](vector-search/README.md)
