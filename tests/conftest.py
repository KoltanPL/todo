import datetime
from typing import TYPE_CHECKING

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
import src.task.task as task_module
from src.task.task import Todo
from src.todo_list.todo_list import TodoList


if TYPE_CHECKING:  # pragma: no cover
    from _pytest.monkeypatch import MonkeyPatch


class _FixedDateTime(datetime.datetime):
    _fixed_now = datetime.datetime(2025, 12, 11, 21, 30, 0, tzinfo=datetime.UTC)

    @classmethod
    def now(cls, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        return cls._fixed_now if tz is None else cls._fixed_now.astimezone(tz)


@pytest.fixture(autouse=True)
def _freeze_datetime(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(task_module, "datetime", _FixedDateTime)


@pytest.fixture
def basic_todo() -> Todo:
    return Todo(
        description="Write tests",
        priority=PriorityEnum.LOW,
        deadline=(_FixedDateTime.now(tz=datetime.UTC) + datetime.timedelta(days=10)).date(),
        tags=["Python", "JavaScript", "Java"],
        status=StatusEnum.IN_PROGRESS,
    )


@pytest.fixture
def todo_1() -> Todo:
    return Todo(
        description="Learn python",
    )


@pytest.fixture
def todo_2() -> Todo:
    return Todo(
        description="Learn js",
    )


@pytest.fixture
def todo_3() -> Todo:
    return Todo(
        description="Learn ts",
    )


@pytest.fixture
def todo_4() -> Todo:
    return Todo(
        description="Learn sql",
    )


@pytest.fixture
def basic_todo_list(todo_1: Todo, todo_2: Todo, todo_3: Todo, todo_4: Todo) -> TodoList:
    return TodoList([todo_1, todo_2, todo_3, todo_4])


@pytest.fixture
def todo_high_priority() -> Todo:
    return Todo(
        description="Learn FastAPI",
        priority=PriorityEnum.HIGH,
        status=StatusEnum.TODO,
        tags=["urgent", "backend"],
        deadline=(_FixedDateTime.now(tz=datetime.UTC) + datetime.timedelta(days=2)).date(),
    )


@pytest.fixture
def todo_low_priority() -> Todo:
    return Todo(
        description="Learn MongoDB",
        priority=PriorityEnum.LOW,
        status=StatusEnum.IN_PROGRESS,
        tags=["backend", "data"],
        deadline=(_FixedDateTime.now(tz=datetime.UTC) + datetime.timedelta(days=30)).date(),
    )


@pytest.fixture
def todo_completed() -> Todo:
    return Todo(
        description="Learn Java",
        priority=PriorityEnum.MEDIUM,
        status=StatusEnum.COMPLETED,
        tags=["backend"],
        deadline=(_FixedDateTime.now(tz=datetime.UTC) + datetime.timedelta(days=15)).date(),
    )


@pytest.fixture
def todo_no_deadline() -> Todo:
    return Todo(
        description="Task without deadline",
        priority=PriorityEnum.MEDIUM,
        status=StatusEnum.TODO,
        tags=["documentation"],
        deadline=None,
    )


@pytest.fixture
def mixed_todo_list(
    todo_high_priority: Todo,
    todo_low_priority: Todo,
    todo_completed: Todo,
    todo_no_deadline: Todo,
) -> TodoList:
    return TodoList([todo_high_priority, todo_low_priority, todo_completed, todo_no_deadline])
