import os
from pathlib import Path

from src.todo_list.todo_list import TodoList


def get_storage_path() -> Path:
    configured_path: str | None = os.getenv('STORAGE_PATH_ENV')
    if not configured_path:
        raise ValueError('Data storage is not configure.')

    return Path(configured_path).expanduser()


def load_todo_list() -> TodoList:
    storage_path = get_storage_path()

    if not storage_path.exists():
        raise ValueError('Data storage is not exists.')

    try:
        raw = storage_path.read_text(encoding='utf-8')
    except OSError as e:
        raise ValueError('Data storage can not read.') from e

    if not raw.strip():
        raise ValueError('Data storage is invalid.')

    try:
        return TodoList.from_json(raw)

    except (ValueError, TypeError) as e:
        raise ValueError('Invalid data storage.') from e


_todo_list = load_todo_list()


def save_todo_list() -> None:
    storage_path = get_storage_path()
    storage_path.write_text(_todo_list.to_json(indent=4), encoding='utf-8')


def get_todo_list() -> TodoList:
    return _todo_list
