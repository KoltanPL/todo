import json

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


def test_to_json_returns_string(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()

    assert isinstance(mtj, str)


def test_to_json_is_valid_json(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()

    parsed = json.loads(mtj)
    assert isinstance(parsed, dict)


def test_to_json_contains_all_fields(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()
    parsed = json.loads(mtj)

    assert set(parsed.keys()) == {"description", "priority", "created_at", "deadline", "tags", "status", "idx"}


def test_to_json_correct_values(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()
    parsed = json.loads(mtj)

    assert parsed["description"] == "Learn FastAPI"
    assert parsed["priority"] == PriorityEnum.HIGH.value
    assert parsed["status"] == StatusEnum.TODO.value
    assert parsed["tags"] == ["urgent", "backend"]
    assert isinstance(parsed["created_at"], str)
    assert isinstance(parsed["deadline"], str) or parsed["deadline"] is None
    assert isinstance(parsed["idx"], str)


def test_to_json_with_indent(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json(indent=2)
    parsed = json.loads(mtj)

    assert isinstance(mtj, str)
    assert "\n" in mtj
    assert "  " in mtj
    assert parsed["description"] == "Learn FastAPI"


def test_to_json_without_indent(todo_high_priority: Todo) -> None:
    mtj = todo_high_priority.to_json()
    parsed = json.loads(mtj)

    assert isinstance(mtj, str)
    assert parsed["description"] == "Learn FastAPI"


def test_from_json_returns_todo(todo_high_priority: Todo) -> None:
    json_str = todo_high_priority.to_json()
    todo_restored = Todo.from_json(json_str)

    assert isinstance(todo_restored, Todo)


def test_from_json_correct_values(todo_high_priority: Todo) -> None:
    json_str = todo_high_priority.to_json()
    todo_restored = Todo.from_json(json_str)

    assert todo_restored.description == "Learn FastAPI"
    assert todo_restored.priority == PriorityEnum.HIGH
    assert todo_restored.status == StatusEnum.TODO
    assert todo_restored.tags == ["urgent", "backend"]


def test_from_json_all_fields(todo_high_priority: Todo) -> None:
    json_str = todo_high_priority.to_json()
    todo_restored = Todo.from_json(json_str)

    assert todo_restored.description == todo_high_priority.description
    assert todo_restored.priority == todo_high_priority.priority
    assert todo_restored.status == todo_high_priority.status
    assert todo_restored.tags == todo_high_priority.tags
    assert todo_restored.deadline == todo_high_priority.deadline
    assert todo_restored.created_at == todo_high_priority.created_at
    assert todo_restored.idx == todo_high_priority.idx


def test_from_json_with_invalid_json() -> None:
    invalid_json = "{ invalid json }"

    with pytest.raises(json.JSONDecodeError):
        Todo.from_json(invalid_json)


def test_from_json_with_non_object_json() -> None:
    json_array = '["not", "an", "object"]'

    with pytest.raises(TypeError, match="Todo JSON must represent an object"):
        Todo.from_json(json_array)

    json_string = '"just a string"'

    with pytest.raises(TypeError, match="Todo JSON must represent an object"):
        Todo.from_json(json_string)

    json_number = "42"

    with pytest.raises(TypeError, match="Todo JSON must represent an object"):
        Todo.from_json(json_number)


def test_from_json_with_missing_fields() -> None:
    incomplete_json = json.dumps({
        "description": "Test",
    })

    with pytest.raises(KeyError):
        Todo.from_json(incomplete_json)


def test_from_json_with_none_deadline() -> None:
    data = {
        "description": "Test task",
        "priority": PriorityEnum.LOW.value,
        "created_at": "2025-01-11T10:00:00+00:00",
        "deadline": None,
        "tags": [],
        "status": StatusEnum.TODO.value,
        "idx": "123e4567-e89b-12d3-a456-426614174000",
    }
    json_str = json.dumps(data)

    todo = Todo.from_json(json_str)
    assert todo.deadline is None


def test_to_json_from_json_roundtrip(todo_high_priority: Todo) -> None:
    json_str = todo_high_priority.to_json()

    todo_restored = Todo.from_json(json_str)

    assert todo_restored.description == todo_high_priority.description
    assert todo_restored.priority == todo_high_priority.priority
    assert todo_restored.status == todo_high_priority.status
    assert todo_restored.tags == todo_high_priority.tags
    assert todo_restored.deadline == todo_high_priority.deadline
    assert todo_restored.created_at == todo_high_priority.created_at
    assert todo_restored.idx == todo_high_priority.idx


def test_to_json_from_json_roundtrip_with_indent(todo_high_priority: Todo) -> None:
    json_with_indent = todo_high_priority.to_json(indent=4)

    todo_restored = Todo.from_json(json_with_indent)

    json_without_indent = todo_restored.to_json()

    parsed_with = json.loads(json_with_indent)
    parsed_without = json.loads(json_without_indent)

    assert parsed_with == parsed_without


def test_to_json_from_json_roundtrip_unicode() -> None:
    todo = Todo(
        description="Test ąćęłńóśźż 🚀",
        priority=PriorityEnum.MEDIUM,
        status=StatusEnum.IN_PROGRESS,
        tags=["unicode", "émoji 😀"],
    )

    json_str = todo.to_json()
    todo_restored = Todo.from_json(json_str)

    assert todo_restored.description == "Test ąćęłńóśźż 🚀"
    assert "émoji 😀" in todo_restored.tags


def test_multiple_roundtrips(todo_high_priority: Todo) -> None:
    todo1 = todo_high_priority

    json1 = todo1.to_json()
    todo2 = Todo.from_json(json1)

    json2 = todo2.to_json()
    todo3 = Todo.from_json(json2)

    json3 = todo3.to_json()
    todo4 = Todo.from_json(json3)

    assert json.loads(json1) == json.loads(json2)
    assert json.loads(json2) == json.loads(json3)

    assert todo4.description == todo1.description
    assert todo4.priority == todo1.priority
    assert todo4.status == todo1.status
    assert todo4.tags == todo1.tags
    assert todo4.deadline == todo1.deadline
    assert todo4.created_at == todo1.created_at
    assert todo4.idx == todo1.idx
