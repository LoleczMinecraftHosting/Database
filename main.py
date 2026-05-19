import json
import ssl
import urllib.request
from http.server import ThreadingHTTPServer

from api.api_core import APIHandler
from core.utils import user_bool_input
from core.logs import log, INFO, DEBUG, CRITICAL
from core.verify import load_auth_map, load_private_key
from core.database import get_database_version, migrate_database, create_database
from core.database.database import Database
from globals import Globals
from config import DATABASE_DIR, AUTH_MAP_LINK, API_PORT, DATABASE_SUPPORTED_VERSION, PRIV_KEY

log(INFO, "---  PROGRAM START ---")
log(INFO, f"USING DATABASE FROM '{DATABASE_DIR}'")

def shutdown(code=1):
    log(INFO, "SHUTDOWN...")

    log(INFO, "--- goodbye ---")
    exit(code)

try:
    with urllib.request.urlopen(AUTH_MAP_LINK, context=ssl.create_default_context()) as r:
        raw_auth_map = json.loads(r.read().decode())
    auth_map = load_auth_map(raw_auth_map)
except Exception as e:
    log(CRITICAL, f"error while getting auth_map from {AUTH_MAP_LINK};\n{e}")
    shutdown(-10)

try:
    private_key = load_private_key(PRIV_KEY)
except Exception as e:
    log(CRITICAL, f"error while loading private key from {PRIV_KEY};\n{e}")
    private_key = False

log(DEBUG, "API GET handlers:\n" +
    json.dumps([tpl for _, _, tpl in APIHandler.routes_get], indent=2))
log(DEBUG, "API POST handlers:\n" +
    json.dumps([tpl for _, _, tpl in APIHandler.routes_post], indent=2))
log(DEBUG, "API DELETE handlers:\n" +
    json.dumps([tpl for _, _, tpl in APIHandler.routes_delete], indent=2))


if not DATABASE_DIR.exists():
    log(CRITICAL, f"database file {DATABASE_DIR} does not exist")
    if user_bool_input(f"create the database at {DATABASE_DIR}?", 30):
        try:
            create_database(DATABASE_DIR, DATABASE_SUPPORTED_VERSION)
        except (RuntimeError, ValueError):
            shutdown(-11)
    else:
        shutdown(2)
db_version = get_database_version(DATABASE_DIR)
if db_version != DATABASE_SUPPORTED_VERSION:
    log(CRITICAL, f"database version {db_version} is not supported;\n"
                  f"expected version {DATABASE_SUPPORTED_VERSION}")
    if db_version < DATABASE_SUPPORTED_VERSION:
        if user_bool_input("autoupdate the database?", 30):
            try:
                migrate_database(
                    DATABASE_DIR, db_version, DATABASE_SUPPORTED_VERSION)
            except (RuntimeError, ValueError):
                shutdown()
        else:
            shutdown()
    else:
        shutdown()
Globals.database = Database(DATABASE_DIR)


log(INFO, "- STARTING API HANDLER -")
with ThreadingHTTPServer(("0.0.0.0", API_PORT), APIHandler) as server:
    server.auth_map, server.seen_nonce, server.private_key = auth_map, {}, private_key
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log(INFO, "server KeyboardInterrupt")
    log(INFO, "closing server")
    server.shutdown()
    server.server_close()

shutdown()
