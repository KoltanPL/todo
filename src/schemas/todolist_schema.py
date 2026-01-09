from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from src.schemas.todo_schema import TodoDict


class TodoListDict(TypedDict):
    tasks: list[TodoDict]
