from datetime import date

import pytest

from src.enums.priority_enum import PriorityEnum
from src.task.task import Todo


def test_str_all_attributes() -> None:
    my_todo = Todo(
        description="WRITE testS", priority=PriorityEnum.HIGH, deadline=date(2025, 12, 15), tags=["python", "testing"]
    )

    assert str(my_todo) == "🔴  Write tests | 📅  2025-12-15 | 🏷️ python, 🏷️ testing"


def test_str_no_tags() -> None:
    my_todo = Todo(
        description="WRITE testS",
        priority=PriorityEnum.HIGH,
        deadline=date(2025, 12, 15),
    )

    assert str(my_todo) == "🔴  Write tests | 📅  2025-12-15 "


def test_str_no_deadline() -> None:
    my_todo = Todo(description="WRITE testS", priority=PriorityEnum.HIGH, deadline=None)

    assert str(my_todo) == "🔴  Write tests | 📅  - "


@pytest.mark.parametrize(
    ("priority", "expected_emoji"),
    [
        (PriorityEnum.HIGH, "🔴"),
        (PriorityEnum.MEDIUM, "🟡"),
        (PriorityEnum.LOW, "🟢"),
    ],
)
def test_str_priority_emoji(priority: PriorityEnum, expected_emoji: str) -> None:
    my_todo = Todo(
        description="WRITE testS",
        priority=priority,
    )

    result = str(my_todo)

    assert result.startswith(expected_emoji)
