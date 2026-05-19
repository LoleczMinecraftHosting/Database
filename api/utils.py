from dataclasses import dataclass
from typing import Callable, Dict
import json
import time


@dataclass
class APIReturn:
    result: dict
    code: int = 200


@dataclass
class APIFunc:
    func: Callable[[object], APIReturn]
    autoauth: bool


def api_get_json(headers: dict, body: bytes) -> dict | None:
    ctype = headers.get("Content-Type", "")
    if ctype != "application/json":
        return None

    if not body:
        return None

    try:
        return json.loads(body.decode("utf-8"))
    except Exception:
        return None


def read_dict(read: dict, read_elements: list) -> tuple[APIReturn | bool, ...]:
    values = [None] * len(read_elements)
    for i, element in enumerate(read_elements):
        readed = read.get(element, None)
        if readed is None:
            return (APIReturn(
                {"error": {"missing value": element}}, 400),
                *values)
        values[i] = readed
    return (True, *values)


NONCE_TTL = 300


def cleanup_seen_nonces(seen_nonce: Dict[object, int]):
    now = time.time()
    for nonce_key, seen_at in list(seen_nonce.items()):
        if now - seen_at > NONCE_TTL:
            del seen_nonce[nonce_key]
