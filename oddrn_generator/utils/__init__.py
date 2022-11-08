def escape(value: any) -> any:
    if isinstance(value, str):
        return value.replace("/", "\\\\")
    else:
        return value


def unescape(value: str) -> str:
    return value.replace("\\\\", "/")
