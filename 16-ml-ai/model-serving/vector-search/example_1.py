# Create a Delta Sync index with managed embeddings
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.vector_search.client import VectorSearchClient
spark.sql("ALTER TABLE main.rag.doc_chunks SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
vsc = VectorSearchClient()
vsc.create_endpoint(name="rag-endpoint", endpoint_type="STANDARD")
index = vsc.create_delta_sync_index(
    endpoint_name="rag-endpoint",
    index_name="main.rag.doc_chunks_index",
    source_table_name="main.rag.doc_chunks",
    pipeline_type="TRIGGERED",
    primary_key="chunk_id",
    embedding_source_column="chunk_text",
    embedding_model_endpoint_name="databricks-gte-large-en")
