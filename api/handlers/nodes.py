from core.database import (
    DBStatus,
    get_node_servers, get_nodes, get_node,
    add_node,
)
from api.api_core import APIHandler
from api.utils import APIReturn, read_dict, api_get_json


@APIHandler.get("/node/{node_id}/servers")
def get_servers_for_node(headers, query, node_id):
    result = get_node_servers(node_id)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "node does not exist"}, code=404)
    return APIReturn(result.data)

@APIHandler.get("/nodes")
def get_all_nodes(headers, query):
    return APIReturn(get_nodes().data)

@APIHandler.get("/node/{node_id}")
def get_one_node(headers, query, node_id):
    result = get_node(node_id)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "node does not exist"}, code=404)
    return APIReturn(result.data)


@APIHandler.post("/add_node", autoauth={"admin"})
def api_add_node(headers, query, data):
    success, node_id, name, address = read_dict(api_get_json(headers, data), ["node_id", "name", "address"])
    if success is not True:
        return success
    result = add_node(node_id, name, address)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.CONFLICT:
        return APIReturn({"error": "already exists"}, code=409)
    return APIReturn({"status": "ok"})
