# Query with a filter, then sync after new docs land
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
index = vsc.get_index(endpoint_name="rag-endpoint", index_name="main.rag.doc_chunks_index")
hits = index.similarity_search(
    query_text="How do I rotate a service principal secret?",
    columns=["chunk_id", "source", "chunk_text"],
    filters={"source": "runbooks"},
    num_results=5, query_type="HYBRID")
index.sync()        # TRIGGERED pipelines update on demand or from a job
