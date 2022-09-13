def escape(value: any) -> str:
    if isinstance(value, str):
        return value.replace("/", "\\\\")


def unescape(value: str) -> str:
    return value.replace("\\\\", "/")
