from os.path import expandvars


def expand(v: str) -> str:
    """Expand envvars."""
    return expandvars(v)
