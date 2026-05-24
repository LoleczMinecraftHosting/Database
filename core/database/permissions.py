from core.utils import make_int, make_str
from .utils import DBReturn, get_database


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

        rows = cursor.fetchall()

        result = {
            "guilds": {},
            "users": {},
            "global": {},
            "roles": {},
        }

        for row in rows:
            subject_type = make_str(row["subject_type"])
            subject_id = make_int(row["subject_id"])
            server_name = make_str(row["server_name"])
            perms = make_int(row["perms"])
            if not subject_type or not server_name or not perms:  # Invalid
                continue

            if subject_type == "guild":
                if subject_id is None:
                    continue
                if subject_id not in result["guilds"]:
                    result["guilds"][subject_id] = {}
                result["guilds"][subject_id][server_name] = perms

            elif subject_type == "user":
                if subject_id is None:
                    continue
                if subject_id not in result["users"]:
                    result["users"][subject_id] = {}
                result["users"][subject_id][server_name] = perms

            elif subject_type == "role":
                if subject_id is None:
                    continue

                if subject_id not in result["roles"]:
                    result["roles"][subject_id] = {}

                result["roles"][subject_id][server_name] = perms

            elif subject_type == "default":
                result["global"][server_name] = perms
        return DBReturn(data=result)
    finally:
        conn.close()
