from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


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
    res = mixed_todo_list.filter_by(tag="backend")

    assert len(res.tasks) == 3
    assert todo_high_priority in res.tasks
    assert todo_low_priority in res.tasks


def test_filter_by_deadline_before(
    mixed_todo_list: TodoList,
    todo_high_priority: Todo,
    todo_completed: Todo,
) -> None:
    cutoff_date = (datetime.now(tz=UTC) + timedelta(days=10)).date()
    result = mixed_todo_list.filter_by(deadline_before=cutoff_date)

    assert len(result.tasks) == 2
    assert todo_high_priority in result.tasks
    assert todo_completed in result.tasks


def test_filter_by_deadline_after(mixed_todo_list: TodoList, todo_low_priority: Todo) -> None:
    cutoff_date = (datetime.now(tz=UTC) + timedelta(days=20)).date()
    result = mixed_todo_list.filter_by(deadline_after=cutoff_date)

    assert len(result.tasks) == 1
    assert result.tasks[0] is todo_low_priority
