import os
from pathlib import Path

from src.todo_list.todo_list import TodoList


def get_storage_path() -> Path:
    """
    Retrieve the configured storage file path.

    The path is read from the environment variable `STORAGE_PATH_ENV`.

    Returns:
        Path: Expanded filesystem path to the storage file.

    Raises:
        ValueError: If the environment variable is not set.
    """
    configured_path: str | None = os.getenv('STORAGE_PATH_ENV')
    if not configured_path:
        raise ValueError('Data storage is not configure.')

    return Path(configured_path).expanduser()


def load_todo_list() -> TodoList:
    """
    Load the TodoList from the configured storage file.

    The function reads the file content, validates it, and deserializes
    it into a TodoList object.

    Returns:
        TodoList: Loaded todo list instance.

    Raises:
        ValueError: If the storage path does not exist.
        ValueError: If the file cannot be read.
        ValueError: If the file content is empty or invalid.
        ValueError: If deserialization fails.
    """
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


_todo_list: TodoList | None = None


def save_todo_list() -> None:
    """
    Persist the current TodoList to the storage file.

    The data is serialized to JSON and written using UTF-8 encoding.
    """
    storage_path = get_storage_path()
    storage_path.write_text(get_todo_list().to_json(indent=4), encoding='utf-8')


def get_todo_list() -> TodoList:
    """
    Get the in-memory TodoList instance.

    Returns:
        TodoList: Currently loaded todo list.
    """
    global _todo_list  # noqa: PLW0603

    if _todo_list is None:
        _todo_list = load_todo_list()

    return _todo_list
