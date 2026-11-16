# FastAPI app calling a serving endpoint on behalf of the user
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
