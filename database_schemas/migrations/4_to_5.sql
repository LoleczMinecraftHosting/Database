BEGIN;


PRAGMA foreign_keys = OFF;

CREATE TABLE permissions_new (
    subject_type TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    server_name TEXT,
    perms INTEGER NOT NULL,

    CHECK (subject_type IN ('default', 'user', 'guild', 'role')),

    UNIQUE (
        subject_type,
        subject_id,
        server_name
    ),

    FOREIGN KEY(server_name) REFERENCES servers(name)
);

INSERT INTO permissions_new (
    subject_type,
    subject_id,
    server_name,
    perms
)
SELECT
    subject_type,
    subject_id,
    server_name,
    perms
FROM permissions;

DROP TABLE permissions;

ALTER TABLE permissions_new RENAME TO permissions;


PRAGMA user_version = 5;

COMMIT;