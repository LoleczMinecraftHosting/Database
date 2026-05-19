from core.database import get_perms
from api.api_core import APIHandler
from api.utils import APIReturn


@APIHandler.get("/get_perms")
def get_permissions(headers, query):
    return APIReturn(get_perms())
