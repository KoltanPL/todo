from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:  # pragma: no cover
    from src.task.task import Todo
    from src.todo_list.todo_list import TodoList


def test_remove_task_idx_in_tasks(basic_todo_list: TodoList, todo_1: Todo) -> None:
    basic_todo_list.remove(todo_1.idx)

    assert len(basic_todo_list.tasks) == 3
    assert todo_1.idx not in [todo.idx for todo in basic_todo_list.tasks]


def test_remove_task_idx_not_in_tasks(basic_todo_list: TodoList, basic_todo: Todo) -> None:
    with pytest.raises(ValueError, match=rf'Task with idx: {basic_todo.idx} not found.'):
        basic_todo_list.remove(basic_todo.idx)
