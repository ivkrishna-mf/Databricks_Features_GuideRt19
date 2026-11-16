# Audit sign-ins and permission changes
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
SELECT event_time, user_identity.email, service_name, action_name, source_ip_address, response.status_code
FROM system.access.audit
WHERE event_date >= current_date() - INTERVAL 7 DAYS
  AND (action_name LIKE '%login%' OR action_name = 'updatePermissions')
ORDER BY event_time DESC""").show(50, truncate=False)
