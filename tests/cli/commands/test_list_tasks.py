from typing import TYPE_CHECKING

from rich.table import Table

from src.cli.commands.list_tasks import list_tasks


if TYPE_CHECKING:
    import pytest


class DummyTodoList:
    """Simple stub for TodoList."""

    def __init__(self, size: int) -> None:
        self._size = size

    def __len__(self) -> int:
        return self._size


def test_list_tasks_when_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Should print a message when no tasks are present.
    """

    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_get_todo_list() -> DummyTodoList:
        return DummyTodoList(0)

    monkeypatch.setattr('src.cli.commands.list_tasks.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.list_tasks.get_todo_list', fake_get_todo_list)

    list_tasks()

    assert len(printed) == 1
    assert '[yellow]No tasks found.[/yellow]' in printed[0]


def test_list_tasks_when_tasks_exist(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Should build a table and print it when tasks exist.
    """

    captured: dict[str, object] = {}

    def fake_print(*args: object, **kwargs: object) -> None:
        if args and isinstance(args[0], Table):
            captured['table'] = args[0]

    def fake_get_todo_list() -> DummyTodoList:
        return DummyTodoList(3)

    def fake_build_tasks_table(todo_list: DummyTodoList) -> Table:
        return Table(title='Tasks')

    monkeypatch.setattr('src.cli.commands.list_tasks.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.list_tasks.get_todo_list', fake_get_todo_list)
    monkeypatch.setattr(
        'src.cli.commands.list_tasks.build_tasks_table',
        fake_build_tasks_table,
    )

    list_tasks()

    table = captured['table']  # type: ignore[arg-type]

    assert isinstance(table, Table)
    assert table.title == 'Tasks'
