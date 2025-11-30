import json
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    """JSON encoder that supports UUID."""

    def default(self, obj):
        if isinstance(obj, UUID):
            return {"__uuid__": str(obj)}
        return super().default(obj)


def json_loads(data: str):
    """JSON loader that restores UUIDs."""

    def object_hook(obj):
        if "__uuid__" in obj:
            return UUID(obj["__uuid__"])
        return obj

    return json.loads(data, object_hook=object_hook)


def json_dumps(obj) -> str:
    """JSON dumper that serializes UUIDs."""
    return json.dumps(obj, cls=JSONEncoder)
