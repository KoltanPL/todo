from typing import TYPE_CHECKING

from rich.table import Table

from src.cli.commands.print_task_summary import print_task_summary


if TYPE_CHECKING:
    from collections.abc import Callable

    import pytest

    from src.task.task import Todo


def extract_rows(table: Table) -> list[tuple[str, str]]:
    """
    Extract rows from a Rich Table.

    Args:
        table (Table): Rich table instance.

    Returns:
        list[tuple[str, str]]: List of rows as (field, value).
    """
    return list(zip(*(col._cells for col in table.columns), strict=False))


def fake_print_collector(storage: dict[str, object]) -> Callable[..., None]:
    """
    Create a fake console.print function that captures Table.

    Args:
        storage (dict[str, object]): Storage for captured objects.

    Returns:
        Callable[..., None]: Fake print function.
    """

    def fake_print(*args: object, **kwargs: object) -> None:
        if args and isinstance(args[0], Table):
            storage['table'] = args[0]

    return fake_print


def test_print_task_summary_calls_console_print_twice(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    calls: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        calls.append(args)

    monkeypatch.setattr('src.cli.commands.print_task_summary.console.print', fake_print)

    print_task_summary(sample_task)

    assert len(calls) == 2


def test_print_task_summary_renders_table(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        'src.cli.commands.print_task_summary.console.print',
        fake_print_collector(captured),
    )

    print_task_summary(sample_task)

    table = captured['table']

    assert isinstance(table, Table)
    assert table.title == 'Current Task'


def test_print_task_summary_contains_correct_values(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        'src.cli.commands.print_task_summary.console.print',
        fake_print_collector(captured),
    )

    print_task_summary(sample_task)

    rows = extract_rows(captured['table'])  # type: ignore[arg-type]

    assert ('Status', sample_task.status.value) in rows
    assert ('Priority', sample_task.priority.name) in rows
    assert ('Description', sample_task.description) in rows
    assert ('Deadline', str(sample_task.deadline)) in rows
    assert ('Tags', ', '.join(sample_task.tags)) in rows


def test_print_task_summary_highlights_field(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        'src.cli.commands.print_task_summary.console.print',
        fake_print_collector(captured),
    )

    print_task_summary(sample_task, highlight_field='status')

    rows = extract_rows(captured['table'])  # type: ignore[arg-type]

    expected = f'[bold green]{sample_task.status.value}[/bold green]'

    assert ('Status', expected) in rows


def test_print_task_summary_handles_empty_tags(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    sample_task.tags = []

    captured: dict[str, object] = {}

    monkeypatch.setattr(
        'src.cli.commands.print_task_summary.console.print',
        fake_print_collector(captured),
    )

    print_task_summary(sample_task)

    rows = extract_rows(captured['table'])  # type: ignore[arg-type]

    assert ('Tags', '-') in rows
