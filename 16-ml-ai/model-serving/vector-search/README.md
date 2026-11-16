# Vector Search

Available since ~2023 · Part of [Model Serving, Foundation Model APIs and AI Gateway](../README.md)

## What it is

Vector Search stores embeddings and answers similarity queries for retrieval-augmented generation, recommendations and semantic search. A Delta Sync index stays in sync with a source Delta table and can compute embeddings for you with a serving endpoint. Hybrid search combines keyword and vector scores.

## How it flows

1. **Source table**: Chunks of text with an id; change data feed enabled.
2. **Delta Sync index**: Embeds new and changed rows automatically.
3. **Endpoint**: Hosts one or more indexes.
4. **Query**: Text or vector in, top-k rows out, with filters.
5. **Use**: Context for an LLM or results for a search box.

```
[Source table] --> [Delta Sync index] --> [Endpoint] --> [Query] --> [Use]
```

## When to choose it

**Choose it when**

- RAG over documents governed in Unity Catalog.
- Semantic search over product catalogs or tickets.

**Pick something else when**

- Exact lookups by key: a table or Lakebase is simpler.

## Senior engineer verdict

> Retrieval quality is mostly chunking and metadata, not the index. I keep chunk text, source, section and permissions columns in the source table, filter on them at query time, and evaluate retrieval separately from generation.

## Examples

### 1. Create a Delta Sync index with managed embeddings

File: [`example_1.py`](example_1.py)

```python
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
```

### 2. Query with a filter, then sync after new docs land

File: [`example_2.py`](example_2.py)

```python
index = vsc.get_index(endpoint_name="rag-endpoint", index_name="main.rag.doc_chunks_index")
hits = index.similarity_search(
    query_text="How do I rotate a service principal secret?",
    columns=["chunk_id", "source", "chunk_text"],
    filters={"source": "runbooks"},
    num_results=5, query_type="HYBRID")
index.sync()        # TRIGGERED pipelines update on demand or from a job
```

## Traps and gotchas

- Delta Sync indexes need change data feed on the source table.
- TRIGGERED sync costs less; CONTINUOUS keeps the index fresher.
