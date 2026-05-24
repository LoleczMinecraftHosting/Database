import json
import sys
import ssl
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit

from core.verify import make_signature_headers, load_private_key, verify_response_signature, load_auth_map
from config import API_PORT, AUTH_MAP_LINK


def read_body():
    print("Body JSON/text. Empty line = no body.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    body = "\n".join(lines)
    if body == "":
        return b""
    return body.encode("utf-8")


def get_path_from_url(url):
    parsed = urlsplit(url)
    path = parsed.path or "/"

    if parsed.query:
        path = f"{path}?{parsed.query}"

    return path


try:
    with request.urlopen(AUTH_MAP_LINK, context=ssl.create_default_context()) as r:
        raw_auth_map = json.loads(r.read().decode())
    auth_map = load_auth_map(raw_auth_map)
except Exception as e:
    print(f"error while getting auth_map from {AUTH_MAP_LINK};\n{e}")
    exit(-10)


url = input("URL: ").strip()
if url.startswith("/"):
    url = f"http://localhost:{API_PORT}{url}"
elif not url.startswith(("http://", "https://")):
    url = "https://" + url
method = input("Method [POST]: ").strip().upper() or "POST"
service = "admin"
key_path = input("Private key path: ").strip() or "admin_priv_key.pem"

body_bytes = read_body()
private_key = load_private_key(key_path)

path = get_path_from_url(url)

headers, nonce = make_signature_headers(
    private_key=private_key,
    method=method,
    path=path,
    body_bytes=body_bytes,
)

headers["X-Service"] = service

if body_bytes:
    headers["Content-Type"] = "application/json"

req = request.Request(
    url=url,
    data=body_bytes if method not in ("GET", "HEAD") else None,
    headers=headers,
    method=method,
)

print()
print("Sending:")
print(method, url)
print(json.dumps(headers, indent=4))

try:
    with request.urlopen(req, timeout=10) as response:
        response_body = response.read()

        print()
        print("Status:", response.status)
        print("Headers:")
        print(response.headers)
        print("Body:")
        print(response_body.decode("utf-8", errors="replace"))
        print("Verified:", verify_response_signature(auth_map["database"], response.status, response_body, response.headers, nonce))

except HTTPError as error:
    response_body = error.read()

    print()
    print("HTTP error:", error.code)
    print("Headers:")
    print(error.headers)
    print("Body:")
    print(response_body.decode("utf-8", errors="replace"))
    print("Verified:", verify_response_signature(auth_map["database"], error.status, response_body, error.headers, nonce))
    sys.exit(1)

except URLError as error:
    print()
    print("URL error:", error)
    sys.exit(1)
