# Ask a Genie space from code
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
