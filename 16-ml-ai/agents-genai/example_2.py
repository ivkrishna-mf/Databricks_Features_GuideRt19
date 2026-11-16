# Evaluate with built-in judges and a custom scorer
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
