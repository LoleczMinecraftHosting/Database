from core.utils import make_str
from .utils import DBReturn, Status, get_database
from .check_utils import node_exists


def get_nodes():
    conn = get_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                address
            FROM nodes
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        data = {}
        for row in rows:
            data[row["id"]] = {
                "name": row["name"],
                "address": row["address"],
            }
        return DBReturn(Status.OK, data=data)
    finally:
        conn.close()

def get_node(node_id):
    node_id = make_str(node_id)
    if not node_id:
        return DBReturn(Status.INVALID_INPUT)

    conn = get_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                address
            FROM nodes
            WHERE id = ?
            """,
            (node_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return DBReturn(Status.NOT_FOUND)
        return DBReturn(
            Status.OK,
            data={
                "id": row["id"],
                "name": row["name"],
                "address": row["address"],
            },
        )
    finally:
        conn.close()


def add_node(node_id, name, address) -> DBReturn:
    node_id = make_str(node_id)
    name = make_str(name)
    address = make_str(address)

    if not node_id or not name or not address:
        return DBReturn(Status.INVALID_INPUT)

    conn = get_database()
    cursor = conn.cursor()
    try:
        if node_exists(node_id, cursor):
            return DBReturn(Status.CONFLICT)

        cursor.execute(
            """
            INSERT INTO nodes (
                id,
                name,
                address
            )
            VALUES (?, ?, ?)
            """,
            (
                node_id,
                name,
                address,
            ),
        )
        conn.commit()
        return DBReturn()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
