ESCAPED_DELIMITER = "\\\\"
DELIMITER = "/"


def escape(value: any) -> any:
    if isinstance(value, str):
        return value.replace(DELIMITER, ESCAPED_DELIMITER)
    else:
        return value


def unescape(value: str) -> str:
    return value.replace(ESCAPED_DELIMITER, DELIMITER)
