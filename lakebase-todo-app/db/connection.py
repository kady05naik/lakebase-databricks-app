import time
import streamlit as st
from psycopg_pool import ConnectionPool
from config import workspace_client, PROJECT_ID, BRANCH_ID, DATABASE_NAME

# Module-level connection state
_postgres_token = None
_last_token_refresh = 0
_connection_pool = None
_endpoint_name = None
_endpoint_host = None


####################################
## Endpoint Discovery
####################################

def get_endpoint_info():
    """Discover the primary endpoint name and host for this branch."""
    global _endpoint_name, _endpoint_host
    if _endpoint_name and _endpoint_host:
        return _endpoint_name, _endpoint_host

    parent = f"projects/{PROJECT_ID}/branches/{BRANCH_ID}"
    endpoints = list(workspace_client.postgres.list_endpoints(parent=parent))
    if not endpoints:
        raise RuntimeError(f"No endpoints found for {parent}")

    _endpoint_name = endpoints[0].name
    ep = workspace_client.postgres.get_endpoint(name=_endpoint_name)
    _endpoint_host = ep.status.hosts.host
    return _endpoint_name, _endpoint_host


####################################
## OAuth Token Management
####################################

def refresh_oauth_token():
    """Generate a fresh database credential (valid ~1 hour)."""
    global _postgres_token, _last_token_refresh
    if _postgres_token is None or time.time() - _last_token_refresh > 2700:  # refresh at 45 min
        print("Refreshing Lakebase Autoscaling database credential")
        try:
            ep_name, _ = get_endpoint_info()
            cred = workspace_client.postgres.generate_database_credential(
                endpoint=ep_name
            )
            _postgres_token = cred.token
            _last_token_refresh = time.time()
        except Exception as e:
            st.error(f"Failed to refresh database credential: {str(e)}")
            st.stop()


####################################
## Connection Pool
####################################

def get_connection_pool():
    """Get or create the connection pool."""
    global _connection_pool
    if _connection_pool is None:
        refresh_oauth_token()
        _, host = get_endpoint_info()
        username = workspace_client.current_user.me().user_name

        conn_string = (
            f"dbname={DATABASE_NAME} "
            f"user={username} "
            f"password={_postgres_token} "
            f"host={host} "
            f"port=5432 "
            f"sslmode=require"
        )
        _connection_pool = ConnectionPool(conn_string, min_size=2, max_size=10)
    return _connection_pool


def get_connection():
    """Get a connection from the pool, recreating if token expired."""
    global _connection_pool

    if _postgres_token is None or time.time() - _last_token_refresh > 2700:
        if _connection_pool:
            _connection_pool.close()
            _connection_pool = None

    return get_connection_pool().connection()
