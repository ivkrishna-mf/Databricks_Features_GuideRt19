# Create an ingestion pipeline with the Python SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.pipelines import IngestionPipelineDefinition, IngestionConfig, TableSpec
w = WorkspaceClient()
p = w.pipelines.create(
    name="erp_ingest", catalog="main", schema="bronze_erp", serverless=True,
    ingestion_definition=IngestionPipelineDefinition(
        ingestion_gateway_id="<gateway-pipeline-id>",
        objects=[IngestionConfig(table=TableSpec(
            source_catalog="erp", source_schema="dbo", source_table="customers",
            destination_catalog="main", destination_schema="bronze_erp"))]))
w.pipelines.start_update(pipeline_id=p.pipeline_id)
