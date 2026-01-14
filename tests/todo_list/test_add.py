from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:  # pragma: no cover
    from src.task.task import Todo
    from src.todo_list.todo_list import TodoList


def test_add_adds_task_to_list(basic_todo_list: TodoList, basic_todo: Todo) -> None:
    basic_todo_list.add(basic_todo)

    assert len(basic_todo_list.tasks) == 5
    assert basic_todo_list.tasks[-1] is basic_todo


def test_add_raises_on_duplicate_idx(basic_todo_list: TodoList, todo_1: Todo) -> None:
    with pytest.raises(ValueError, match=r'Duplicate Todo index values detected'):
        basic_todo_list.add(todo_1)
