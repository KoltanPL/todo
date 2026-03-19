from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest
from rich.table import Table

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.todo_list.todo_list import TodoList
from src.ui.tables import build_tasks_table


if TYPE_CHECKING:
    from collections.abc import Iterator
    from datetime import date


@dataclass
class DummyTask:
    description: str
    priority: PriorityEnum | int
    status: StatusEnum
    deadline: date | str | None
    tags: list[str]


class DummyTodoList(TodoList):
    def __iter__(self) -> Iterator[DummyTask]:
        return iter(self._tasks)


@pytest.fixture
def sample_tasks() -> DummyTodoList:
    """Provide a list of sample tasks."""
    obj = DummyTodoList()
    obj._tasks = [
        DummyTask(
            description='Task 1',
            priority=PriorityEnum.HIGH,
            status=StatusEnum.TODO,
            deadline=None,
            tags=['a', 'b'],
        ),
        DummyTask(
            description='Task 2',
            priority=PriorityEnum.LOW,
            status=StatusEnum.COMPLETED,
            deadline='2026-01-01',
            tags=[],
        ),
    ]
    return obj


def extract_rows(table: Table) -> list[tuple[str, ...]]:
    return list(zip(*(col._cells for col in table.columns), strict=False))


def test_build_tasks_table_returns_table(sample_tasks: DummyTodoList) -> None:
    table = build_tasks_table(sample_tasks)

    assert isinstance(table, Table)
    assert table.title == 'Todo List'


def test_build_tasks_table_columns(sample_tasks: DummyTodoList) -> None:
    table = build_tasks_table(sample_tasks)

    headers = [col.header for col in table.columns]

    assert headers == ['Id', 'Status', 'Priority', 'Description', 'Deadline', 'Tags']


def test_build_tasks_table_rows_content(sample_tasks: DummyTodoList) -> None:
    table = build_tasks_table(sample_tasks)

    rows = extract_rows(table)

    assert ('1', ' todo ', '[red]HIGH[/red]', 'Task 1', 'None', 'a, b') in rows
    assert ('2', 'completed'.center(6), '[green]LOW[/green]', 'Task 2', '2026-01-01', '-') in rows


def test_build_tasks_table_priority_default_color(sample_tasks: DummyTodoList) -> None:
    class FakePriority:
        name = 'CUSTOM'

    sample_tasks._tasks[0].priority = FakePriority()  # type: ignore[assignment]

    table = build_tasks_table(sample_tasks)

    rows = extract_rows(table)

    assert any('[white]CUSTOM[/white]' in row[2] for row in rows)
