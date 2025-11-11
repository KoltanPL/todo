import datetime
from typing import TYPE_CHECKING

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
import src.task.task as task_module
from src.task.task import Todo


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
