from typing import TYPE_CHECKING, TypeGuard, cast


if TYPE_CHECKING:  # pragma: no cover
    from src.schemas.todo_schema import TodoDict


def is_todo_dict(obj: object) -> TypeGuard[TodoDict]:
    if not isinstance(obj, dict):
        return False

    data = cast('dict[str, object]', obj)

    required_keys: dict[str, type[object] | tuple[type[object], ...]] = {
        'description': str,
        'priority': int,
        'created_at': str,
        'deadline': (str, type(None)),
        'tags': list,
        'status': str,
        'idx': str,
    }

    if set(required_keys) != set(obj):
        return False

    for key, expected_type in required_keys.items():
        if not isinstance(data[key], expected_type):
            return False

    tags = data['tags']
    if not isinstance(tags, list):  # pragma: no cover
        return False

    return all(isinstance(tag, str) for tag in tags)
