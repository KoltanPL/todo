from datetime import UTC, date, datetime, timezone
from uuid import UUID, uuid4

import pytest

from src.enums.priority_enum import PriorityEnum
import src.task.task as task_module
from src.task.task import Todo


def test_create_todo_with_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)

    class DummyDateTime:
        @classmethod
        def now(cls, tz: timezone | None = None) -> datetime:  # noqa: ARG003
            return fixed_datetime

    monkeypatch.setattr(task_module, 'datetime', DummyDateTime)

    t = Todo('Write tests')
    assert t.description == 'Write tests'
    assert t.priority == PriorityEnum.MEDIUM
    assert t.deadline is None
    assert t.tags == []
    assert t.created_at == fixed_datetime
    assert isinstance(t.idx, UUID)
    assert t.idx.version == 4


def test_todo_description_too_short() -> None:
    with pytest.raises(ValueError, match=r'must be at least 3 characters.'):
        Todo('a')


def test_idx_accepts_uuid_str() -> None:
    idx = 'de184248-44f2-4944-a209-a6097846da17'
    t = Todo('Write tests', idx=idx)
    assert t.idx == UUID(idx, version=4)


def test_idx_accepts_uuid_object() -> None:
    idx = uuid4()
    t = Todo('Write tests', idx=idx)
    assert t.idx == idx


def test_idx_invalid_str_raises() -> None:
    with pytest.raises(ValueError, match='badly formed hexadecimal UUID string'):
        Todo('Write tests', idx='123456')


def test_todo_deadline_none() -> None:
    t = Todo('Write tests', deadline=None)
    assert t.deadline is None


def test_todo_deadline_invalid() -> None:
    with pytest.raises(ValueError, match=r'Deadline .* is invalid, date should be from the future.'):
        Todo('Write tests', deadline=date(2024, 1, 1), created_at=datetime(2024, 2, 10, tzinfo=UTC))


def test_todo_deadline_valid() -> None:
    t = Todo('Write tests', deadline=date(2024, 3, 1), created_at=datetime(2024, 2, 10, tzinfo=UTC))
    assert t.deadline == date(2024, 3, 1)
