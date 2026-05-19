from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Callable, List, Tuple, Pattern
import json
import re

from core.logs import log, INFO, WARNING, ERROR
from core.verify import verify_signature, make_response_signature_headers
from .utils import APIReturn, APIFunc, cleanup_seen_nonces


def _compile_template(template: str) -> Pattern[str]:
    var = re.compile(r'{([a-zA-Z_][a-zA-Z0-9_]*)}')
    pattern = var.sub(r'(?P<\1>[^/]+)', template)
    return re.compile(f'^{pattern}$')


class APIHandler(BaseHTTPRequestHandler):
    # regex, handler, template
    routes_get: List[Tuple[Pattern[str], APIFunc, str]] = []
    routes_post: List[Tuple[Pattern[str], APIFunc, str]] = []
    routes_delete: List[Tuple[Pattern[str], APIFunc, str]] = []

    def log_message(self, format, *args):
        pass

    def _handle(self, table, read_body):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        client_ip = self._get_client_ip()

        handler, params = self._match(table, path)
        if handler is None:
            log(WARNING,
                f"API {self.command} 404 <{client_ip}> {self.path}")
            self.send_error(404)
            return

        body = b""
        if read_body:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

        verified = self._authenticate(body)
        if not verified and handler.autoauth:
            log(WARNING, f"API UNAUTH {self.command} 401 "
                         f"<{client_ip}> {self.path}")
            self.reply(APIReturn({"error": "unauthorized"}, 401))
            return

        try:
            if read_body:
                res: APIReturn = handler.func(self.headers, query, body, **params)
            else:
                res: APIReturn = handler.func(self.headers, query, **params)
        except Exception as e:
            log(ERROR, f"API ERROR {self.command} 500 <{client_ip}> {self.path}\n E; {e}")
            self.reply(APIReturn({"error": "Internal server error"}, 500))
            return

        formatted = json.dumps(res.result, indent=2, ensure_ascii=False)
        name = self.headers.get("FromService", client_ip)
        log(INFO,
            f"API {self.command} {res.code} <{name}> "
            f"{self.path} {formatted}")
        self.reply(res)

    def do_GET(self):
        self._handle(self.routes_get, read_body=False)

    def do_POST(self):
        self._handle(self.routes_post, read_body=True)

    def do_DELETE(self):
        self._handle(self.routes_delete, read_body=True)

    def do_OPTIONS(self):
        log(INFO, f"API OPTIONS 204 <{self.address_string()}>",)
        self.send_response(204)
        self._apply_cors()
        self.end_headers()

    def reply(self, ret: APIReturn):
        data = json.dumps(ret.result).encode("utf-8")

        self.send_response(ret.code)
        self._apply_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if self.server.private_key:
            for header, value in make_response_signature_headers(self.server.private_key, self.headers, ret.code, data).items():
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(data)

    @classmethod
    def get(cls, template: str, autoauth: bool = True):
        def decorator(func: Callable):
            regex = _compile_template(template)
            cls.routes_get.append((regex, APIFunc(func, autoauth), template))
            return func
        return decorator

    @classmethod
    def post(cls, template: str, autoauth: bool = True):
        def decorator(func: Callable):
            regex = _compile_template(template)
            cls.routes_post.append((regex, APIFunc(func, autoauth), template))
            return func
        return decorator

    @classmethod
    def delete(cls, template: str, autoauth: bool = True):
        def decorator(func: Callable):
            regex = _compile_template(template)
            cls.routes_delete.append(
                (regex, APIFunc(func, autoauth), template))
            return func
        return decorator


    def _authenticate(self, body):
        service = self.headers.get("X-Service", "")
        public_key = self.server.auth_map.get(service.lower(), False)
        if not public_key:
            return
        result = verify_signature(public_key, self.command, self.path, body, self.headers, self.server.seen_nonce)
        cleanup_seen_nonces(self.server.seen_nonce)
        return result

    def _match(self, table: List[Tuple[Pattern[str], APIFunc, str]],
               path: str):
        for regex, handler, template in table:
            m = regex.match(path)
            if m:
                return handler, m.groupdict()
        return None, {}

    def _apply_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers",
                         "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, DELETE, OPTIONS")

    def _get_client_ip(self):
        xff = self.headers.get('X-Forwarded-For')
        if xff:
            return xff.split(',')[0].strip()

        xrip = self.headers.get('X-Real-IP')
        if xrip:
            return xrip.strip()

        return self.client_address[0]