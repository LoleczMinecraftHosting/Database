import time

from core.utils import make_int, make_str
from .utils import DBReturn, Status, get_database
from .check_utils import server_exists, node_exists


def add_server_config(
    name, display_name,
    node_id,
    host=None,
    port=None,
    ram_min_mb=2048,
    ram_max_mb=4096,
    start_command=None,
    stop_command=None,
    working_directory=None,
):
    name, display_name = make_str(name), make_str(display_name)
    node_id = make_str(node_id)
    host = make_str(host)
    port = make_int(port)
    ram_min_mb = make_int(ram_min_mb) or 2048
    ram_max_mb = make_int(ram_max_mb) or 4096
    start_command = make_str(start_command)
    stop_command = make_str(stop_command)
    working_directory = make_str(working_directory)

    if not name or not display_name or not node_id:
        return DBReturn(Status.INVALID_INPUT)
    if ram_min_mb < 0 or ram_max_mb < ram_min_mb:
        return DBReturn(Status.INVALID_INPUT)
    if port is not None and not 1 <= port <= 65535:
        return DBReturn(Status.INVALID_INPUT)

    conn = get_database()
    cursor = conn.cursor()

    try:
        if server_exists(name, cursor):
            return DBReturn(Status.CONFLICT)
        if not node_exists(node_id, cursor):
            return DBReturn(Status.NOT_FOUND)

        cursor.execute(
            """
            INSERT INTO servers (
                name,
                display_name,
                node_id,
                status_updated_at,
                host,
                port,
                ram_min_mb,
                ram_max_mb,
                start_command,
                stop_command,
                working_directory
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                display_name,
                node_id,
                int(time.time()),
                host,
                port,
                ram_min_mb,
                ram_max_mb,
                start_command,
                stop_command,
                working_directory,
            ),
        )
        conn.commit()
        return DBReturn(Status.OK)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()