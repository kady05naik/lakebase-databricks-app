from psycopg import sql
from db.connection import get_connection


def get_schema_name(SCHEMA_NAME='public'):
    return SCHEMA_NAME


def init_database():
    """Initialize the todos table."""
    schema = get_schema_name()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(schema)))
            cur.execute(sql.SQL("""
                CREATE TABLE IF NOT EXISTS {}.todos (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """).format(sql.Identifier(schema)))
            conn.commit()
            return True
