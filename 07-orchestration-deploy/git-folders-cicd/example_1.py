# Create a Git folder and check out a tag
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
repo = w.repos.create(url="https://github.com/acme/orders-platform.git", provider="gitHub",
                      path="/Workspace/Users/de@acme.com/orders-platform")
w.repos.update(repo_id=repo.id, tag="v1.4.0")        # detached at a release tag
