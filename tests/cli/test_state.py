from __future__ import annotations

import importlib
from pathlib import Path
import re
from typing import TYPE_CHECKING, cast

import pytest

from src.cli import state
import src.cli.state as state_module


if TYPE_CHECKING:
    from src.todo_list.todo_list import TodoList


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Provide a temporary file path for storage."""
    return tmp_path / 'data.json'


def test_get_storage_path_reads_env(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    path = state.get_storage_path()

    assert path == temp_file


def test_get_storage_path_raises_when_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv('STORAGE_PATH_ENV', raising=False)

    with pytest.raises(ValueError, match=re.escape('Data storage is not configure.')):
        state.get_storage_path()


def test_load_todo_list_file_not_exists(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    with pytest.raises(ValueError, match=re.escape('Data storage is not exists.')):
        state.load_todo_list()


def test_load_todo_list_empty_file(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    temp_file.write_text('', encoding='utf-8')
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    with pytest.raises(ValueError, match=re.escape('Data storage is invalid.')):
        state.load_todo_list()


def test_load_todo_list_read_error(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    temp_file.write_text('', encoding='utf-8')
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    def fake_read_text(*_: object, **__: object) -> str:
        raise OSError()

    monkeypatch.setattr(Path, 'read_text', fake_read_text)

    with pytest.raises(ValueError, match=re.escape('Data storage can not read.')):
        state.load_todo_list()


def test_load_todo_list_invalid_json(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    temp_file.write_text('invalid', encoding='utf-8')
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    def fake_from_json(_: str) -> TodoList:
        raise ValueError()

    monkeypatch.setattr('src.todo_list.todo_list.TodoList.from_json', fake_from_json)

    with pytest.raises(ValueError, match=re.escape('Invalid data storage.')):
        state.load_todo_list()


def test_load_todo_list_success(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    temp_file.write_text('{}', encoding='utf-8')
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    class Dummy:
        pass

    def fake_from_json(_: str) -> Dummy:
        return Dummy()

    monkeypatch.setattr('src.todo_list.todo_list.TodoList.from_json', fake_from_json)

    result = state.load_todo_list()

    assert isinstance(result, Dummy)


def test_save_todo_list(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    class Dummy:
        @staticmethod
        def to_json(indent: int) -> str:
            _ = indent
            return 'data'

    monkeypatch.setattr(state, '_todo_list', Dummy())

    state.save_todo_list()

    assert temp_file.read_text(encoding='utf-8') == 'data'


def test_get_todo_list_returns_global(monkeypatch: pytest.MonkeyPatch) -> None:
    class Dummy:
        pass

    dummy = Dummy()
    monkeypatch.setattr(state, '_todo_list', dummy)

    assert state.get_todo_list() is dummy


def test_module_import_does_not_loads_todo_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv('STORAGE_PATH_ENV', raising=False)

    module = cast('type(state_module)', importlib.reload(state_module))

    assert module._todo_list is None


def test_get_todo_list_loads_once_after_import(monkeypatch: pytest.MonkeyPatch, temp_file: Path) -> None:
    temp_file.write_text('{}', encoding='utf-8')
    monkeypatch.setenv('STORAGE_PATH_ENV', str(temp_file))

    class Dummy:
        pass

    calls = {'count': 0}

    def fake_from_json(_: str) -> Dummy:
        calls['count'] += 1
        return Dummy()

    monkeypatch.setattr('src.todo_list.todo_list.TodoList.from_json', fake_from_json)

    module = cast('type(state_module)', importlib.reload(state_module))

    assert module._todo_list is None

    first = module.get_todo_list()
    second = module.get_todo_list()

    assert first is second
    assert calls['count'] == 1
