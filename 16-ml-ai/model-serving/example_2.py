# Call a foundation model with the OpenAI client
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
client = WorkspaceClient().serving_endpoints.get_open_ai_client()
out = client.chat.completions.create(
    model="databricks-claude-sonnet-4",          # any chat endpoint name in your workspace
    messages=[{"role": "user", "content": "Summarize this ticket in one sentence: ..."}],
    max_tokens=100)
print(out.choices[0].message.content)
