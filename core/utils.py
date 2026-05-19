from threading import Thread


def make_int(value) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    if isinstance(value, float):
        return int(value)
    return None


def make_str(value) -> str | None:
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        return str(value)
    return None


def user_bool_input(message: str, timeout: int = -1):
    def _user_input(full_message: str, result: list):
        result[0] = input(full_message)
    formatted = f"{message} (Y/n); "
    user_output: list = [None]
    user_input_thread = Thread(
        target=_user_input, args=[formatted, user_output], daemon=True)
    user_input_thread.start()
    user_input_thread.join(timeout)
    if user_output[0] is None:
        print("- input timeouted -")
        return False
    return user_output[0].lower() in ('y', 'yes')