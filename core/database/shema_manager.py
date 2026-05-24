from .utils import run_sql_file, get_database_version
from database_schemas.schemas import FULL_SCHEMAS, MIGRATIONS
from core.logs import log, ERROR, INFO, SUCCESS
from pathlib import Path


def create_database(db_path, version):
    if version not in FULL_SCHEMAS:
        log(ERROR, f"cannot create database with version <{version}>")
        raise ValueError(f"cannot create database with version <{version}>")
    file = FULL_SCHEMAS[version]
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        run_sql_file(db_path, file)
    except Exception as err:
        log(ERROR, f"Error while creating database;\n{err}")
    if get_database_version(db_path) != version:
        log(ERROR, f"creating database with version <{version}> failed")
        if path.is_file():
            log(INFO, "removing broken database file")
            path.unlink()
        raise RuntimeError(f"creating database with version <{version}> failed")
    log(SUCCESS, f"database created at {db_path}")


def migrate_database(path, current, target):
    # 1- ensure all migrations are available
    for i in range(current, target):
        if i not in MIGRATIONS:
            log(ERROR, f"missing migration from version <{i}> to <{i+1}>")
            raise ValueError(
                f"missing migration from version <{i}> to <{i+1}>")

    # 2- run migrations
    for i in range(current, target):
        sql_path = MIGRATIONS[i]
        log(INFO, f"migrating database from version <{i}> to <{i+1}>")
        try:
            run_sql_file(path, sql_path)
        except Exception as err:
            log(ERROR, f"Error while creating migrating database;\n{err}")
        if get_database_version(path) != i + 1:
            log(ERROR, f"migration from version <{i}> to <{i+1}> failed")
            raise RuntimeError(f"migration from version <{i}> to <{i+1}> failed")
    log(SUCCESS, f"database succesfully migrated to {target}")