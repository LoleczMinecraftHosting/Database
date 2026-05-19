from dataclasses import dataclass


@dataclass
class LogType:
    name: str


DEBUG = LogType("DEBUG")
INFO = LogType("INFO")
WARNING = LogType("WARNING")
ERROR = LogType("ERROR")
CRITICAL = LogType("CRITICAL")
SUCCESS = LogType("SUCCESS")


_TYPE_WIDTH = max(len(t.name) for t in [
    DEBUG, INFO, WARNING, ERROR, CRITICAL, SUCCESS
])
_SPACE_PAD = " " * _TYPE_WIDTH


def _plain_log(log_text):
    print(log_text)


def log(log_type: LogType, message: str):
    message = str(message)
    lines = message.split("\n")
    header = f"{log_type.name.ljust(_TYPE_WIDTH)} || {lines[0]}"
    if len(lines) > 1:
        ind = f"{_SPACE_PAD}  | "
        body = "\n".join(f"{ind}{line}" for line in lines[1:])
        _plain_log(f"{header}\n{body}")
    else:
        _plain_log(header)
