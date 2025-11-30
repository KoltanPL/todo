from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:  # pragma: no cover
    from src.task.task import Todo
    from src.todo_list.todo_list import TodoList


def test_get_task_idx_exists(basic_todo_list: TodoList, todo_1: Todo) -> None:
    assert basic_todo_list.get(todo_1.idx) is todo_1


def test_remove_task_idx_not_in_tasks(basic_todo_list: TodoList, basic_todo: Todo) -> None:
    with pytest.raises(ValueError, match=rf"Task with idx: {basic_todo.idx} not found."):
        basic_todo_list.get(basic_todo.idx)
