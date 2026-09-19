BEGIN;


PRAGMA foreign_keys = ON;

ALTER TABLE servers
ADD COLUMN player_count INTEGER;

ALTER TABLE servers
ADD COLUMN max_player_count INTEGER;

ALTER TABLE servers
ADD COLUMN player_nicknames TEXT DEFAULT "[]"
CHECK (
    CASE
        WHEN player_nicknames IS NULL THEN 1
        WHEN json_valid(player_nicknames)
            THEN json_type(player_nicknames) = 'array'
        ELSE 0
    END
);

ALTER TABLE servers
ADD COLUMN ram_usage_mb INTEGER;

ALTER TABLE servers
ADD COLUMN cpu_usage_percent REAL;


PRAGMA user_version = 6;

COMMIT;