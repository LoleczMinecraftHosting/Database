BEGIN;

PRAGMA foreign_keys = ON;



CREATE TABLE permissions (
    subject_type TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    server_name TEXT NOT NULL,
    perms INTEGER NOT NULL,

    CHECK (subject_type IN ('default', 'user', 'guild', 'role')),

    PRIMARY KEY (
        subject_type,
        subject_id,
        server_name
    )
);


CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);


CREATE TABLE servers (
    name TEXT PRIMARY KEY,

    display_name TEXT NOT NULL,
    node_id TEXT,

    status TEXT NOT NULL DEFAULT 'unknown',
    status_updated_at INTEGER,

    host TEXT,
    port INTEGER,

    ram_min_mb INTEGER NOT NULL DEFAULT 2048,
    ram_max_mb INTEGER NOT NULL DEFAULT 4096,

    start_command TEXT,
    stop_command TEXT,
    working_directory TEXT,

    FOREIGN KEY(node_id) REFERENCES nodes(id)
);
CREATE INDEX idx_servers_node
ON servers (
    node_id
);


PRAGMA user_version = 2;

COMMIT;