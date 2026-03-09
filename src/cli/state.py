from typing import TYPE_CHECKING

from src.bootstrap import bootstrap_tasks


if TYPE_CHECKING:
    from src.todo_list.todo_list import TodoList

_todo_list = bootstrap_tasks()


def get_todo_list() -> TodoList:
    return _todo_list
