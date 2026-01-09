from datetime import UTC, timedelta
from typing import TYPE_CHECKING

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from tests.conftest import _FixedDateTime


if TYPE_CHECKING:  # pragma: no cover
    from src.task.task import Todo
    from src.todo_list.todo_list import TodoList


def test_filter_by_priority(mixed_todo_list: TodoList, todo_high_priority: Todo) -> None:
    res = mixed_todo_list.filter_by(priority=PriorityEnum.HIGH)

    assert len(res.tasks) == 1
    assert res.tasks[0] is todo_high_priority


def test_filter_by_status(mixed_todo_list: TodoList, todo_completed: Todo) -> None:
    res = mixed_todo_list.filter_by(status=StatusEnum.COMPLETED)

    assert len(res.tasks) == 1
    assert res.tasks[0] is todo_completed


def test_filter_by_tag(mixed_todo_list: TodoList, todo_high_priority: Todo, todo_low_priority: Todo) -> None:
    res = mixed_todo_list.filter_by(tag='backend')

    assert len(res.tasks) == 3
    assert todo_high_priority in res.tasks
    assert todo_low_priority in res.tasks


def test_filter_by_deadline_before(
    mixed_todo_list: TodoList,
    todo_high_priority: Todo,
    todo_completed: Todo,
) -> None:
    cutoff_date = (_FixedDateTime.now(tz=UTC) + timedelta(days=16)).date()
    res = mixed_todo_list.filter_by(deadline_before=cutoff_date)

    assert len(res.tasks) == 2
    assert todo_high_priority in res.tasks
    assert todo_completed in res.tasks


def test_filter_by_deadline_after(mixed_todo_list: TodoList, todo_low_priority: Todo) -> None:
    cutoff_date = (_FixedDateTime.now(tz=UTC) + timedelta(days=20)).date()
    res = mixed_todo_list.filter_by(deadline_after=cutoff_date)

    assert len(res.tasks) == 1
    assert res.tasks[0] is todo_low_priority


def test_filter_by_multiple_criteria(mixed_todo_list: TodoList, todo_high_priority: Todo) -> None:
    res = mixed_todo_list.filter_by(
        priority=PriorityEnum.HIGH,
        status=StatusEnum.TODO,
        tag='urgent',
        deadline_before=(_FixedDateTime.now(tz=UTC) + timedelta(days=365)).date(),
    )

    assert len(res.tasks) == 1
    assert res.tasks[0] is todo_high_priority


def test_filter_by_no_criteria(mixed_todo_list: TodoList) -> None:
    res = mixed_todo_list.filter_by()

    assert len(res.tasks) == 4


def test_filter_by_no_matches(mixed_todo_list: TodoList) -> None:
    res = mixed_todo_list.filter_by(priority=PriorityEnum.HIGH, status=StatusEnum.COMPLETED)

    assert len(res.tasks) == 0


def test_filter_by_task_without_deadline_excluded(
    mixed_todo_list: TodoList,
    todo_no_deadline: Todo,
) -> None:
    cutoff_date = (_FixedDateTime.now(tz=UTC) + timedelta(days=100)).date()
    res = mixed_todo_list.filter_by(deadline_before=cutoff_date)

    assert todo_no_deadline not in res.tasks


def test_filter_by_custom_function(mixed_todo_list: TodoList) -> None:
    res = mixed_todo_list.filter_by(custom_filter=lambda todo: 'learn' in todo.description.lower())

    assert len(res.tasks) == 3
