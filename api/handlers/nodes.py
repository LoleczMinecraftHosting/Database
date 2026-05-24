from core.database import add_node, DBStatus
from api.api_core import APIHandler
from api.utils import APIReturn, read_dict, api_get_json


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
