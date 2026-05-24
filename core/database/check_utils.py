from sqlite3 import Cursor


def server_exists(server_name: str, cursor: Cursor):
    cursor.execute(
        """
        SELECT 1
        FROM servers
        WHERE name = ?
        LIMIT 1
        """,
        (server_name,),
    )
    return cursor.fetchone() is not None


def node_exists(node_id: str, cursor: Cursor):
    cursor.execute(
        """
        SELECT 1
        FROM nodes
        WHERE id = ?
        LIMIT 1
        """,
        (node_id,),
    )
    return cursor.fetchone() is not None
