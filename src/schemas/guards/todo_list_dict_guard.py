from typing import TYPE_CHECKING, TypeGuard, cast

from src.schemas.guards.todo_dict_guard import is_todo_dict


if TYPE_CHECKING:  # pragma: no cover
    from src.schemas.todolist_schema import TodoListDict


def is_todolist_dict(value: object) -> TypeGuard[TodoListDict]:
    if not isinstance(value, dict):
        return False

    if set(value) != {'tasks'}:
        return False

    data = cast('dict[str, object]', value)

    tasks = data['tasks']

    if not isinstance(tasks, list):
        return False

    return all(is_todo_dict(task) for task in tasks)
