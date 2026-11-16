databricks secrets create-scope crm
databricks secrets put-secret crm api_key --string-value "$CRM_API_KEY"
databricks secrets put-acl crm sp-orders-pipeline READ
databricks secrets list-secrets crm
