import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path):
        self.path = Path(path)
        self.connection = None

    def connect(self):
        if self.connection is not None:
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row

        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA busy_timeout = 5000")
        self.connection.execute("PRAGMA foreign_keys = ON")

    def close(self):
        if self.connection is None:
            return

        self.connection.close()
        self.connection = None

    def commit(self):
        self.connect()
        self.connection.commit()

    def rollback(self):
        self.connect()
        self.connection.rollback()

    def cursor(self):
        self.connect()
        return self.connection.cursor()