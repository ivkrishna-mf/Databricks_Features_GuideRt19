# Trace an app with autologging and a decorator
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import mlflow
from databricks.sdk import WorkspaceClient
mlflow.openai.autolog()
mlflow.set_experiment("/Shared/support-agent")
client = WorkspaceClient().serving_endpoints.get_open_ai_client()

@mlflow.trace
def answer(question: str) -> str:
    docs = index.similarity_search(query_text=question, columns=["chunk_text"], num_results=3)
    context = "\n".join(r[0] for r in docs["result"]["data_array"])
    out = client.chat.completions.create(model="databricks-claude-sonnet-4",
        messages=[{"role": "system", "content": "Answer only from the context."},
                  {"role": "user", "content": context + "\n\nQuestion: " + question}])
    return out.choices[0].message.content
