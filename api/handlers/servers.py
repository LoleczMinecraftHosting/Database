from core.database import (
    DBStatus,
    get_servers, get_server_config,
    add_server_config,
    edit_server_close_time,
    edit_server_display_name, edit_server_host,
    edit_server_node, edit_server_ram, edit_server_start_command, edit_server_stop_command,
    edit_server_working_directory,
    update_server_status,
)
from api.api_core import APIHandler
from api.utils import APIReturn, read_dict, api_get_json


@APIHandler.get("/servers")
def get_all_servers(headers, query):
    return APIReturn(get_servers().data)

@APIHandler.get("/server/{server_name}")
def get_server(headers, query, server_name):
    result = get_server_config(server_name)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn(result.data)


@APIHandler.post("/server/{server_name}", autoauth={"admin"})
def post_add_server(headers, query, data, server_name):
    success, display_name, node_id, close_time, host, port, min_ram_mb, max_ram_mb, start_command, stop_command, directory = read_dict(api_get_json(headers, data), ["display_name", "node_id", "close_time", "host", "port", "min_ram_mb", "max_ram_mb", "start_command", "stop_command", "directory"])
    if success is not True:
        return success
    result = add_server_config(
        name=server_name, display_name=display_name,
        node_id=node_id, close_time=close_time, host=host, port=port,
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


@APIHandler.post("/server/{server_name}/close_time", autoauth={"admin"})
def post_edit_server_close_time(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_close_time(name=server_name, close_time=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/display_name", autoauth={"admin"})
def post_edit_server_display_name(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_display_name(name=server_name, display_name=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/node", autoauth={"admin"})
def post_edit_server_node(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_node(name=server_name, node_id=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/start_command", autoauth={"admin"})
def post_edit_server_start_command(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_start_command(name=server_name, start_command=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/stop_command", autoauth={"admin"})
def post_edit_server_stop_command(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_stop_command(name=server_name, stop_command=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/working_directory", autoauth={"admin"})
def post_edit_server_working_directory(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = edit_server_working_directory(name=server_name, working_directory=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/host", autoauth={"admin"})
def post_edit_server_host(headers, query, data, server_name):
    success, host, port = read_dict(api_get_json(headers, data), ["host", "port"])
    if success is not True:
        return success
    result = edit_server_host(name=server_name, host=host, port=port)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})

@APIHandler.post("/server/{server_name}/ram", autoauth={"admin"})
def post_edit_server_ram(headers, query, data, server_name):
    success, min_ram_mb, max_ram_mb = read_dict(api_get_json(headers, data), ["min_ram_mb", "max_ram_mb"])
    if success is not True:
        return success
    result = edit_server_ram(name=server_name, ram_min_mb=min_ram_mb, ram_max_mb=max_ram_mb)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})


@APIHandler.post("/server/{server_name}/status")
def post_update_server_status(headers, query, data, server_name):
    new_value = api_get_json(headers, data)
    result = update_server_status(name=server_name, status=new_value)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})
