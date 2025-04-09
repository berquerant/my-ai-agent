import shlex
from os.path import expandvars


def expand_quote(v: str) -> str:
    return shlex.quote(expandvars(v))
