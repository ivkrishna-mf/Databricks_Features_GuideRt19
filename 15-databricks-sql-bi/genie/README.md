# Genie (natural-language analytics)

Available since ~2024

## What it is

Genie lets business users ask questions in plain language over a curated set of tables. Authors pick the tables or metric views, add instructions, example SQL and trusted queries; Genie writes SQL, runs it on a warehouse and shows the answer with the query. Genie spaces are now called Genie Agents, and a Conversation API lets apps embed them.

## How it flows

1. **Author curates**: Tables, metric views, instructions, sample questions.
2. **User asks**: In plain language.
3. **Genie writes SQL**: Using metadata, comments and examples.
4. **Runs on warehouse**: With the asking user's permissions.
5. **Feedback**: Thumbs and corrections improve the space.

```
[Author curates] --> [User asks] --> [Genie writes SQL] --> [Runs on warehouse] --> [Feedback]
```

## When to choose it

**Choose it when**

- Self-service questions on a well-modeled domain.
- Embedding conversational analytics in an app or chat tool.

**Pick something else when**

- Pointing Genie at hundreds of raw tables. Quality depends on curation.

## Senior engineer verdict

> Genie is only as good as the metadata. Before launching a space I add table and column comments, declare primary and foreign keys, move key KPIs into a metric view and write five trusted example queries. That work also improves every other tool.

## Examples

### 1. Ask a Genie space from code

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
msg = w.genie.start_conversation_and_wait(space_id="<space-id>",
                                         content="What was revenue by region last month?")
for a in msg.attachments or []:
    if a.query:
        print(a.query.query)      # generated SQL
    if a.text:
        print(a.text.content)
follow = w.genie.create_message_and_wait(space_id="<space-id>", conversation_id=msg.conversation_id,
                                         content="Only for EMEA, by week")
```

### 2. Prepare tables so Genie understands them

File: [`example_2.py`](example_2.py)

```python
spark.sql("COMMENT ON TABLE main.gold.fact_orders IS 'One row per order line. Amount is net of tax in EUR.'")
spark.sql("ALTER TABLE main.gold.fact_orders ALTER COLUMN region COMMENT 'Sales region: EMEA, AMER or APAC'")
spark.sql("ALTER TABLE main.gold.fact_orders ADD CONSTRAINT fk_cust FOREIGN KEY (customer_sk) REFERENCES main.gold.dim_customer")
```

## Traps and gotchas

- Genie runs queries with the asking user's permissions; users still need access to the data.
- Answers include the SQL so users can verify them.
