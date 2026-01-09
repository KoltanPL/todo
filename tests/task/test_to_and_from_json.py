import datetime
import json
from uuid import UUID

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


def test_to_json_contains_all_fields(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()
    parsed = json.loads(mtj)

    assert set(parsed.keys()) == {'description', 'priority', 'created_at', 'deadline', 'tags', 'status', 'idx'}


def test_to_json_correct_values(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()
    parsed = json.loads(mtj)

    assert parsed['description'] == 'Learn FastAPI'
    assert parsed['priority'] == 3
    assert parsed['status'] == 'todo'
    assert parsed['tags'] == ['urgent', 'backend']
    assert parsed['created_at'] == '2025-12-11T21:30:00+00:00'
    assert parsed['deadline'] == '2025-12-13'
    assert parsed['idx'] == '7f4deca0-44b7-413a-80d7-550fedb1dc6a'


def test_to_json_with_indent(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json(indent=2)
    parsed = json.loads(mtj)

    assert isinstance(mtj, str)
    assert '\n' in mtj
    assert '  ' in mtj
    assert parsed['description'] == 'Learn FastAPI'


def test_from_json_returns_todo() -> None:
    json_str = (
        '{"description": "Learn FastAPI", "priority": 3, "created_at": "2026-01-14T19:52:00.737625+00:00",'
        ' "deadline": "2026-01-16", "tags": ["urgent", "backend"], "status": "todo",'
        ' "idx": "7f4deca0-44b7-413a-80d7-550fedb1dc6a"}'
    )
    todo_restored = Todo.from_json(json_str)

    assert isinstance(todo_restored, Todo)


def test_from_json_correct_values() -> None:
    json_str = (
        '{"description": "Learn FastAPI", "priority": 3, "created_at": "2026-01-14T19:52:00.737625+00:00",'
        ' "deadline": "2026-01-16", "tags": ["urgent", "backend"], "status": "todo",'
        ' "idx": "7f4deca0-44b7-413a-80d7-550fedb1dc6a"}'
    )
    todo_restored = Todo.from_json(json_str)

    assert isinstance(todo_restored, Todo)
    assert todo_restored.description == 'Learn FastAPI'
    assert todo_restored.priority == PriorityEnum.HIGH
    assert todo_restored.status == StatusEnum.TODO
    assert todo_restored.tags == ['urgent', 'backend']
    assert todo_restored.deadline == datetime.date(2026, 1, 16)
    assert todo_restored.created_at == datetime.datetime(2026, 1, 14, 19, 52, 0, 737625, tzinfo=datetime.UTC)
    assert todo_restored.idx == UUID('7f4deca0-44b7-413a-80d7-550fedb1dc6a')


def test_from_json_with_invalid_json() -> None:
    invalid_json = '{ invalid json }'

    with pytest.raises(json.JSONDecodeError):
        Todo.from_json(invalid_json)


def test_from_json_with_json_array() -> None:
    json_array = '[{"x": 42}]'

    with pytest.raises(TypeError, match=r'Invalid Todo JSON structure.'):
        Todo.from_json(json_array)


def test_from_json_with_missing_fields() -> None:
    incomplete_json = json.dumps({
        'description': 'Test',
    })

    with pytest.raises(TypeError, match=r'Invalid Todo JSON structure.'):
        Todo.from_json(incomplete_json)


def test_from_json_with_none_deadline() -> None:
    data = {
        'description': 'Test task',
        'priority': PriorityEnum.LOW.value,
        'created_at': '2025-01-11T10:00:00+00:00',
        'deadline': None,
        'tags': [],
        'status': StatusEnum.TODO.value,
        'idx': '123e4567-e89b-12d3-a456-426614174000',
    }
    json_str = json.dumps(data)

    todo = Todo.from_json(json_str)
    assert todo.deadline is None
