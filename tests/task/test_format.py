from datetime import UTC, timedelta

from src.enums.status_enum import StatusEnum
from src.task.task import Todo
from tests.conftest import _FixedDateTime


def test_format_short(basic_todo: Todo) -> None:
    formatted = format(basic_todo, "short")

    assert formatted == "[✗] Write tests (10 days left)"


def test_format_long(basic_todo: Todo) -> None:
    formatted = format(basic_todo, "long")

    assert f"{type(basic_todo).__name__} '{basic_todo.description}'" in formatted
    assert f"idx: {basic_todo.idx}" in formatted
    assert f"status: {basic_todo.status.value}" in formatted
    assert "created_at:" in formatted
    assert f"deadline: {basic_todo.deadline}" in formatted
    assert f"priority: {basic_todo.priority.name.capitalize()}" in formatted

    for t in basic_todo.tags:
        assert f"🏷️ {t}" in formatted


def test_format_falls_back_to_str(basic_todo: Todo) -> None:
    formatted = format(basic_todo, "unknown-format")
    assert formatted == str(basic_todo)


def test_format_empty_uses_str(basic_todo: Todo) -> None:
    formatted = format(basic_todo, "")
    assert formatted == str(basic_todo)


def test_format_short_status_symbol() -> None:
    todo_done = Todo(
        description="Test",
        status=StatusEnum.COMPLETED,
        deadline=_FixedDateTime.now(tz=UTC).date() + timedelta(days=5),
    )

    todo_pending = Todo(
        description="Test",
        status=StatusEnum.TODO,
        deadline=_FixedDateTime.now(tz=UTC).date() + timedelta(days=5),
    )

    assert format(todo_done, "short").startswith("[✓]")
    assert format(todo_pending, "short").startswith("[✗]")


def test_format_tags_empty() -> None:
    todo = Todo(
        description="No tags",
        tags=None,
        deadline=_FixedDateTime.now(tz=UTC).date() + timedelta(days=3),
    )

    formatted_long = format(todo, "long")
    assert "tags:" in formatted_long
