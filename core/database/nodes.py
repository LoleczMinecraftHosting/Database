from core.utils import make_str
from .utils import DBReturn, Status, get_database
from .check_utils import node_exists


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