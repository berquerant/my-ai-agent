def read_file_or(v: str | None) -> str | None:
    """Read file v (@FILE) or just v."""
    if v is None:
        return None
    if not v.startswith("@"):
        return v
    with open(v.lstrip("@")) as f:
        return f.read()
