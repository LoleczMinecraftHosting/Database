import re

from config import HONEYPOTS_DIR

# regex, filename, content_type
HONEYPOTS = [
        (
        re.compile(r"(?:^|/)\.env(?:\.[a-z0-9_-]+)*(?=/|$)", re.I),
        ".env",
        "text/plain"
    ),
    (
        re.compile(r"(?:^|/)auth\.json(?:\.[a-z0-9_-]+)*(?=/|$)", re.I),
        "auth.json",
        "application/json"
    ),
    (
        re.compile(r"(?:^|/)schema\.rb(?:\.[a-z0-9_-]+)*(?=/|$)", re.I),
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