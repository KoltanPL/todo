from typing import TYPE_CHECKING
from uuid import uuid4

import pytest


if TYPE_CHECKING:
    from src.task.task import Todo
    from src.todo_list.todo_list import TodoList


def test_len_returns_number_of_tasks(mixed_todo_list: TodoList) -> None:
    assert len(mixed_todo_list) == 4


def test_iter_returns_tasks_in_order(
    mixed_todo_list: TodoList,
    todo_high_priority: Todo,
    todo_low_priority: Todo,
    todo_completed: Todo,
    todo_no_deadline: Todo,
) -> None:
    it = iter(mixed_todo_list)

    assert next(it) == todo_high_priority
    assert next(it) == todo_low_priority
    assert next(it) == todo_completed
    assert next(it) == todo_no_deadline

    with pytest.raises(StopIteration):
        next(it)


def test_contains_returns_true_if_uuid_exists(mixed_todo_list: TodoList, todo_high_priority: Todo) -> None:
    assert todo_high_priority.idx in mixed_todo_list


def test_contains_returns_false_if_uuid_not_exists(mixed_todo_list: TodoList) -> None:
    assert uuid4() not in mixed_todo_list


def test_getitem_returns_correct_task(
    mixed_todo_list: TodoList,
    todo_high_priority: Todo,
    todo_no_deadline: Todo,
) -> None:
    assert mixed_todo_list[0] is todo_high_priority
    assert mixed_todo_list[3] is todo_no_deadline
    assert mixed_todo_list[-4] is todo_high_priority
    assert mixed_todo_list[-1] is todo_no_deadline


def test_getitem_index_error(mixed_todo_list: TodoList) -> None:
    with pytest.raises(IndexError):
        _ = mixed_todo_list[5]
