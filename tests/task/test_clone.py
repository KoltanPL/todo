from datetime import UTC, timedelta
from typing import TYPE_CHECKING

from tests.conftest import _FixedDateTime


if TYPE_CHECKING:  # pragma: no cover
    from src.task.task import Todo


def test_clone_copies_core_fields_and_sets_created_at_now(basic_todo: Todo) -> None:
    new_todo = basic_todo.clone()

    assert new_todo is not basic_todo
    assert new_todo.description == basic_todo.description
    assert new_todo.priority == basic_todo.priority
    assert new_todo.deadline == basic_todo.deadline
    assert new_todo.tags == basic_todo.tags
    assert new_todo.tags is not basic_todo.tags
    assert new_todo.status == basic_todo.status
    assert new_todo.created_at == _FixedDateTime.now(tz=UTC)
    assert new_todo.idx != basic_todo.idx


def test_clone_nulls_past_deadline(basic_todo: Todo) -> None:
    basic_todo._deadline = (_FixedDateTime.now(tz=UTC) - timedelta(days=10)).date()
    new_todo = basic_todo.clone()

    assert new_todo.deadline is None


def test_clone_preserves_none_deadline(basic_todo: Todo) -> None:
    basic_todo._deadline = None
    new_todo = basic_todo.clone()

    assert new_todo.deadline is None
