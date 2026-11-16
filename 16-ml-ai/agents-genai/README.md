# Agents, Agent Bricks and MLflow 3 evaluation

**Major feature** · Available since ~2024

## What it is

Agent Bricks builds common agents from a description and your data with little code: knowledge assistants over documents, information extraction, and supervisors that route between agents and Genie. For custom agents, you write code with any framework, log it with MLflow, and deploy it to Model Serving. MLflow 3 traces every step and evaluates quality with built-in LLM judges and your own scorers, offline and in production.

## How it flows

1. **Build**: Agent Bricks, or code with LangGraph, OpenAI SDK or plain Python and tools (UC functions, Vector Search, Genie).
2. **Trace**: MLflow captures each LLM call, tool call and retrieval.
3. **Evaluate**: mlflow.genai.evaluate with judges such as Correctness, Safety, RetrievalGroundedness.
4. **Deploy**: Register in Unity Catalog, serve behind AI Gateway, review app for experts.
5. **Monitor**: The same scorers run on sampled production traces.

```
[Build] --> [Trace] --> [Evaluate] --> [Deploy] --> [Monitor]
```

## When to choose it

**Choose it when**

- Agent Bricks: a standard pattern and you want a good result fast.
- Custom code: unusual tools, control flow or integration needs.

**Pick something else when**

- Shipping an agent without an evaluation set. Without one you cannot tell whether a prompt change helped.

## Senior engineer verdict

> Evaluation is the product. I start with 30 to 50 real questions with expected answers from domain experts, run them on every change, and add every production failure to the set. Tracing turns 'the bot was wrong' into 'retrieval missed the runbook chunk', which is a fix you can actually make.

## Examples

### 1. Trace an app with autologging and a decorator

File: [`example_1.py`](example_1.py)

```python
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
```

### 2. Evaluate with built-in judges and a custom scorer

File: [`example_2.py`](example_2.py)

```python
import mlflow
from mlflow.genai.scorers import Correctness, RelevanceToQuery, Safety, scorer

@scorer
def short_enough(outputs) -> bool:
    return len(outputs.split()) <= 120

eval_data = [
    {"inputs": {"question": "How do I rotate a service principal secret?"},
     "expectations": {"expected_response": "Create a new OAuth secret, update consumers, then delete the old one."}},
]
results = mlflow.genai.evaluate(data=eval_data, predict_fn=answer,
                                scorers=[Correctness(), RelevanceToQuery(), Safety(), short_enough])
```

## Traps and gotchas

- MLflow 3 evaluation runs only the scorers you list; nothing runs by default.
- predict_fn receives the keys of inputs as keyword arguments.
