from core.database import add_server_config, DBStatus
from api.api_core import APIHandler
from api.utils import APIReturn, read_dict, api_get_json


@APIHandler.post("/server/{server_name}", autoauth={"admin"})
def post_add_server(headers, query, data, server_name):
    success, display_name, node_id, host, port, min_ram_mb, max_ram_mb, start_command, stop_command, directory = read_dict(api_get_json(headers, data), ["display_name", "node_id", "host", "port", "min_ram_mb", "max_ram_mb", "start_command", "stop_command", "directory"])
    if success is not True:
        return success
    result = add_server_config(
        name=server_name, display_name=display_name,
        node_id=node_id, host=host, port=port,
        ram_min_mb=min_ram_mb, ram_max_mb=max_ram_mb,
        start_command=start_command, stop_command=stop_command,
        working_directory=directory
    )
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.CONFLICT:
        return APIReturn({"error": "already exists"}, code=409)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "node does not exist"}, code=404)
    return APIReturn({"status": "ok"})
