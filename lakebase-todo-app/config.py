import os
from databricks import sdk

# Configuration
# Environment variables are set in app.yaml
# The branch and database use standard defaults that match what Lakebase creates automatically
PROJECT_ID = os.getenv("LAKEBASE_PROJECT_ID", "default")
BRANCH_ID = os.getenv("LAKEBASE_BRANCH_ID", "production")
DATABASE_NAME = os.getenv("LAKEBASE_DATABASE_NAME", "databricks_postgres")

# Shared workspace client
workspace_client = sdk.WorkspaceClient()
