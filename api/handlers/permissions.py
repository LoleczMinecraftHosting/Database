from core.database import DBStatus, get_perms, set_perm, remove_perm
from api.api_core import APIHandler
from api.utils import APIReturn, read_dict, api_get_json


@APIHandler.get("/get_perms")
def get_permissions(headers, query):
    return APIReturn(get_perms().data)


@APIHandler.post("/set_perm", autoauth={"admin"})
def post_set_perm(headers, query, data):
    success, subject_type, subject_id, server_name, perms = read_dict(api_get_json(headers, data), ["subject_type", "subject_id", "server_name", "perms"])
    if success is not True:
        return success
    result = set_perm(subject_type, subject_id, server_name, perms)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "server does not exist"}, code=404)
    return APIReturn({"status": "ok"})


@APIHandler.delete("/remove_perm", autoauth={"admin"})
def delete_remove_perm(headers, query, data):
    success, subject_type, subject_id, server_name = read_dict(api_get_json(headers, data), ["subject_type", "subject_id", "server_name"])
    if success is not True:
        return success
    result = remove_perm(subject_type, subject_id, server_name)
    if result.status == DBStatus.INVALID_INPUT:
        return APIReturn({"error": "invalid input"}, code=400)
    if result.status == DBStatus.NOT_FOUND:
        return APIReturn({"error": "permission does not exist"}, code=404)
    return APIReturn({"status": "ok"})