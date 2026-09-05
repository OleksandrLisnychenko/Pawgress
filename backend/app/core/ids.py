from ulid import ULID


def new_id() -> str:
    """Generate an app-side ULID primary key — never rely on DB auto-increment."""
    return str(ULID())
