from pathlib import Path

HOME = Path.home()
DIR = Path(__file__).parent

IN_PROD = False
DATABASE_SUPPORTED_VERSION = 1

DATABASE_DEFINITIONS_DIR = DIR / "database_schemas"
DATABASE_SCHEMA_MIGRATIONS_DIR = DATABASE_DEFINITIONS_DIR / "migrations"
DATABASE_SCHEMA_FULL_DIR = DATABASE_DEFINITIONS_DIR / "full"
AUTH_MAP_LINK = "https://minecraft.loleczkowo.com/auth_map.json"
PRIV_KEY = DIR / "priv_key.pem"

if IN_PROD:
    DATABASE_DIR = DIR/"database.db"
    API_PORT = 35000
else:
    DATABASE_DIR = DIR/"debug.db"
    API_PORT = 35000
