# Create an endpoint for a UC model
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
