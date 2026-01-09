import json
from typing import TYPE_CHECKING, Any, cast

import pytest

import src.todo_list.todo_list as todo_list_module
from src.todo_list.todo_list import TodoList


if TYPE_CHECKING:
    from types import ModuleType

    from _pytest.monkeypatch import MonkeyPatch

    from src.task.task import Todo
    from tests.todo_list.conftest import _TodoStub


def _valid_payload(todos: list[_TodoStub]) -> dict[str, Any]:
    return {'tasks': [todo.to_dict() for todo in todos]}


def test_to_json_returns_valid_json_and_schema(todos: list[_TodoStub], patch_dependencies: ModuleType) -> None:
    tl = TodoList(cast('list[Todo]', todos))

    raw = tl.to_json()
    parsed = json.loads(raw)

    assert parsed == tl.to_dict()
    assert set(parsed.keys()) == {'tasks'}
    assert isinstance(parsed['tasks'], list)
    assert len(parsed['tasks']) == len(todos)


def test_to_json_uses_utf8_not_ascii_escape(todos: list[_TodoStub], patch_dependencies: ModuleType) -> None:
    tl = TodoList(cast('list[Todo]', todos))

    raw = tl.to_json()

    assert 'Zażółć gęślą jaźń' in raw
    assert '\\u' not in raw


def test_from_json_raises_on_invalid_json(patch_dependencies: ModuleType) -> None:
    with pytest.raises(json.JSONDecodeError):
        TodoList.from_json('{not_valid_json')


def test_from_json_calls_guard_and_raises_type_error_when_invalid_structure(
    patch_dependencies: ModuleType, monkeypatch: MonkeyPatch
) -> None:
    seen: dict[str, Any] = {}

    def _guard(value: object) -> bool:
        seen['payload'] = value

        return False

    monkeypatch.setattr(todo_list_module, 'is_todolist_dict', _guard, raising=True)

    raw = json.dumps({'tasks': 'not a list'})

    with pytest.raises(TypeError, match=r'Invalid TodoList JSON structure.'):
        TodoList.from_json(raw)

    assert 'payload' in seen
    assert seen['payload'] == {'tasks': 'not a list'}


def test_from_json_roundtrip_equals_by_dict(
    todos: list[_TodoStub], monkeypatch: MonkeyPatch, patch_dependencies: ModuleType
) -> None:
    def _guard(value: object) -> bool:
        return isinstance(value, dict) and set(value) == {'tasks'} and isinstance(value['tasks'], list)  # type: ignore[argtype]

    monkeypatch.setattr(todo_list_module, 'is_todolist_dict', _guard, raising=True)

    tl = TodoList(cast('list[Todo]', todos))

    raw = tl.to_json()

    parsed = TodoList.from_json(raw)

    assert tl.to_dict() == parsed.to_dict()
    assert [task.idx for task in tl] == [task.idx for task in parsed]
