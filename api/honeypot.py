import re

from config import HONEYPOTS_DIR

# regex, filename, content_type
HONEYPOTS = [
    (
        re.compile(r"/\.env(?:\.[a-zA-Z0-9_-]+)?"),
        "env.txt",
        "text/plain"
    ),
    (
        re.compile(r"/auth\.json"),
        "auth.json",
        "application/json"
    ),
    (
        re.compile(r"/schema\.rb"),
        "schema.rb",
        "text/plain"
    ),
]


def get_honeypot(path):
    for regex, filename, content_type in HONEYPOTS:
        if regex.fullmatch(path):
            file = HONEYPOTS_DIR / filename
            return content_type, file.read_bytes()
    return None