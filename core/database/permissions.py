from core.utils import make_int, make_str
from .utils import DBReturn, Status, get_database
from .check_utils import server_exists


VALID_SUBJECT_TYPES = {"default", "user", "guild", "role"}
RESULT_KEYS = {
    "guild": "guilds",
    "user": "users",
    "role": "roles",
}


def _perm_subject(subject_type, subject_id):
    if subject_type == "default":
        return subject_type, "default"

    return subject_type, subject_id


def get_perms():
    conn = get_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                subject_type,
                subject_id,
                server_name,
                perms
            FROM permissions
            ORDER BY
                subject_type,
                subject_id,
                server_name
            """
        )
        result = {
            "guilds": {},
            "users": {},
            "global": {},
            "roles": {},
        }
        for row in cursor.fetchall():
            subject_type = make_str(row["subject_type"])
            subject_id = make_str(row["subject_id"])
            server_name = make_str(row["server_name"] or "*")
            perms = make_int(row["perms"])
            if not subject_type or not server_name or perms is None:
                continue

            if subject_type == "default":
                result["global"][server_name] = perms
                continue
            result_key = RESULT_KEYS.get(subject_type)
            if result_key is None:
                continue
            if subject_id not in result[result_key]:
                result[result_key][subject_id] = {}
            result[result_key][subject_id][server_name] = perms
        return DBReturn(data=result)
    finally:
        conn.close()


def set_perm(subject_type, subject_id, server_name, perms):
    subject_type = make_str(subject_type)
    subject_id = make_str(subject_id)
    server_name = make_str(server_name)
    perms = make_int(perms)
    if subject_type not in VALID_SUBJECT_TYPES:
        return DBReturn(Status.INVALID_INPUT)
    if not subject_type or not server_name or perms is None:
        return DBReturn(Status.INVALID_INPUT)
    if subject_type != "default" and not subject_id:
        return DBReturn(Status.INVALID_INPUT)

    subject_type, subject_id = _perm_subject(subject_type, subject_id)
    conn = get_database()
    cursor = conn.cursor()
    try:
        if server_name == "*":
            server_name = None
        elif not server_exists(server_name, cursor):
            return DBReturn(Status.NOT_FOUND)

        cursor.execute(
            """
            INSERT INTO permissions (
                subject_type,
                subject_id,
                server_name,
                perms
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT (
                subject_type,
                subject_id,
                server_name
            )
            DO UPDATE SET perms = excluded.perms
            """,
            (
                subject_type,
                subject_id,
                server_name,
                perms,
            ),
        )

        conn.commit()
        return DBReturn()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def remove_perm(subject_type, subject_id, server_name):
    subject_type = make_str(subject_type)
    subject_id = make_str(subject_id)
    server_name = make_str(server_name)
    if subject_type not in VALID_SUBJECT_TYPES:
        return DBReturn(Status.INVALID_INPUT)
    if not subject_type or not server_name:
        return DBReturn(Status.INVALID_INPUT)
    if subject_type != "default" and not subject_id:
        return DBReturn(Status.INVALID_INPUT)

    subject_type, subject_id = _perm_subject(subject_type, subject_id)
    conn = get_database()
    cursor = conn.cursor()
    try:
        if server_name == "*":
            cursor.execute(
                """
                DELETE FROM permissions
                WHERE subject_type = ?
                AND subject_id = ?
                AND server_name IS NULL
                """,
                (
                    subject_type,
                    subject_id,
                ),
            )
        else:
            cursor.execute(
                """
                DELETE FROM permissions
                WHERE subject_type = ?
                AND subject_id = ?
                AND server_name = ?
                """,
                (
                    subject_type,
                    subject_id,
                    server_name,
                ),
            )

        if cursor.rowcount == 0:
            return DBReturn(Status.NOT_FOUND)

        conn.commit()
        return DBReturn()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
