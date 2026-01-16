from typing import TYPE_CHECKING, TypeGuard


if TYPE_CHECKING:  # pragma: no cover
    from src.schemas.todo_schema import TodoDict


def is_todo_dict(obj: object) -> TypeGuard[TodoDict]:
    if not isinstance(obj, dict):
        return False

    required_keys = {
        'description': str,
        'priority': int,
        'created_at': str,
        'deadline': (str, type(None)),
        'tags': list,
        'status': str,
        'idx': str,
    }

    if len(required_keys) != len(obj):
        return False

    for key, expected_type in required_keys.items():
        if key not in obj:
            return False
        if not isinstance(obj[key], expected_type):
            return False

    return all(isinstance(tag, str) for tag in obj['tags'])
