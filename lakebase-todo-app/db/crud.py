from psycopg import sql
from db.connection import get_connection
from db.schema import get_schema_name


def add_todo(task):
    """Insert a new todo item."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(
                sql.SQL("INSERT INTO {}.todos (task) VALUES (%s)").format(sql.Identifier(schema)),
                (task.strip(),)
            )
            conn.commit()


def get_todos():
    """Fetch all todo items, newest first."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(
                sql.SQL("SELECT id, task, completed, created_at FROM {}.todos ORDER BY created_at DESC").format(sql.Identifier(schema))
            )
            return cur.fetchall()


def toggle_todo(todo_id):
    """Toggle the completed status of a todo item."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(
                sql.SQL("UPDATE {}.todos SET completed = NOT completed WHERE id = %s").format(sql.Identifier(schema)),
                (todo_id,)
            )
            conn.commit()


def delete_todo(todo_id):
    """Delete a todo item by ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(
                sql.SQL("DELETE FROM {}.todos WHERE id = %s").format(sql.Identifier(schema)),
                (todo_id,)
            )
            conn.commit()
