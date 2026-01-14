from typing import TYPE_CHECKING, TypedDict  # pragma: no cover


if TYPE_CHECKING:  # pragma: no cover
    from src.schemas.todo_schema import TodoDict  # pragma: no cover


class TodoListDict(TypedDict):  # pragma: no cover
    tasks: list[TodoDict]
