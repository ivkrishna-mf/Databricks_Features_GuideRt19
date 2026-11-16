# Create a service principal and add it to a group
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import AccountClient
from databricks.sdk.service import iam
a = AccountClient()                   # account host and account id from the profile
sp = a.service_principals.create(display_name="sp-orders-pipeline")
grp = next(a.groups.list(filter='displayName eq "data_pipelines"'))
a.groups.patch(id=grp.id, operations=[iam.Patch(op=iam.PatchOp.ADD, path="members",
                                                value=[{"value": sp.id}])],
               schemas=[iam.PatchSchema.URN_IETF_PARAMS_SCIM_API_MESSAGES_2_0_PATCH_OP])
