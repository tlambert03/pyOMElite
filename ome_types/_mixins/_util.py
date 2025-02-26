import uuid


def new_uuid() -> str:
    """Generate a new UUID."""
    return f"urn:uuid:{uuid.uuid4()}"
