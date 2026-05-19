BEGIN;

PRAGMA foreign_keys = ON;



CREATE TABLE IF NOT EXISTS permissions (
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



PRAGMA user_version = 1;

COMMIT;