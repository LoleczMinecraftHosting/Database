import sqlite3
import enum
from dataclasses import dataclass
from typing import Any
from config import DATABASE_DIR


def get_database():
    connection = sqlite3.connect(DATABASE_DIR)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA busy_timeout = 5000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def run_sql_file(run_path, sql_file_path):
    conn = sqlite3.connect(run_path)
    try:
        with open(sql_file_path, "r", encoding="utf8") as f:
            sql = f.read()
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def get_database_version(path):
    conn = sqlite3.connect(path)
    try:
        cur = conn.execute("PRAGMA user_version")
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    finally:
        conn.close()


class Status(enum.Enum):
    OK = 0
    NOT_FOUND = 1
    INVALID_INPUT = 2
    CONFLICT = 3


@dataclass
class DBReturn:
    status: Status = Status.OK
    data: Any = None
