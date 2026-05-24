BEGIN;

CREATE INDEX IF NOT EXISTS idx_servers_node
ON servers (
    node_id
);

PRAGMA user_version = 2;

COMMIT;