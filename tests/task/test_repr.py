from datetime import UTC, date, datetime
from uuid import UUID

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


def test_repr_contains_all_fields() -> None:
    my_todo = Todo(
        description="Write tests",
        priority=PriorityEnum.HIGH,
        created_at=datetime(2025, 11, 16, 12, 0, tzinfo=UTC),
        deadline=date(2026, 1, 15),
        tags=["python", "testing"],
        status=StatusEnum.TODO,
        idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"),
    )

    r = repr(my_todo)

    assert (
        r == "Todo(description='Write tests', priority=PriorityEnum(3), "
        "created_at=datetime.datetime(2025, 11, 16, 12, 0, tzinfo=datetime.timezone.utc), "
        "deadline=datetime.date(2026, 1, 15), tags=['python', 'testing'], status=StatusEnum(\"todo\"), "
        "idx=UUID('931f66ba-99a0-484e-8b19-4866c2f51721'))"
    )


def test_repr_contains_correct_values() -> None:
    my_todo = Todo(
        description="Write tests",
        priority=PriorityEnum.LOW,
        created_at=datetime(2025, 11, 16, 12, 0, tzinfo=UTC),
        deadline=date(2026, 1, 15),
        tags=["python", "testing"],
        status=StatusEnum.IN_PROGRESS,
        idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"),
    )

    r = repr(my_todo)

    assert "description='Write tests'" in r
    assert "priority=PriorityEnum(1)" in r
    assert "created_at=datetime.datetime(2025, 11, 16, 12, 0, tzinfo=datetime.timezone.utc)" in r
    assert "deadline=datetime.date(2026, 1, 15)" in r
    assert "tags=['python', 'testing']" in r
    assert "deadline=datetime.date(2026, 1, 15)" in r
    assert "idx=UUID('931f66ba-99a0-484e-8b19-4866c2f51721')" in r


@pytest.mark.parametrize(
    "priority",
    [
        PriorityEnum.HIGH,
        PriorityEnum.MEDIUM,
        PriorityEnum.LOW,
    ],
)
def test_repr_priority_values(priority: PriorityEnum) -> None:
    my_todo = Todo(description="Write tests", priority=priority)
    r = repr(my_todo)

    expected_fragment = f"priority=PriorityEnum({priority.value})"
    assert expected_fragment in r


def test_repr_handles_none_values() -> None:
    my_todo = Todo(
        description="Write tests",
        deadline=None,
        tags=None,
    )

    r = repr(my_todo)

    assert "deadline=None" in r
    assert "tags=[]" in r
