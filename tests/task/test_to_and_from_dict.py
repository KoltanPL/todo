from datetime import datetime
from uuid import UUID

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


def test_to_dict_correct(todo_high_priority: Todo) -> None:
    mtd = todo_high_priority.to_dict()

    assert isinstance(mtd, dict)
    assert isinstance(mtd["description"], str)
    assert isinstance(mtd["priority"], int)
    assert isinstance(mtd["created_at"], str)
    assert isinstance(mtd["tags"], list)
    assert isinstance(mtd["status"], str)
    assert isinstance(mtd["idx"], str)
    assert mtd.keys() == {"description", "priority", "created_at", "deadline", "tags", "status", "idx"}
    assert mtd["description"] == "Learn FastAPI"
    assert mtd["priority"] == PriorityEnum.HIGH.value
    assert mtd["deadline"] is None or isinstance(mtd["deadline"], str)
    assert mtd["tags"] == ["urgent", "backend"]
    assert mtd["status"] == StatusEnum.TODO


def test_from_dict_correct(todo_high_priority: Todo) -> None:
    mtd = todo_high_priority.to_dict()

    tfd = Todo.from_dict(mtd)

    assert isinstance(tfd, Todo)
    assert tfd.description == "Learn FastAPI"
    assert tfd.priority == PriorityEnum.HIGH
    assert tfd.status == StatusEnum.TODO
    assert tfd.tags == ["urgent", "backend"]
    assert tfd.deadline == todo_high_priority.deadline
    assert tfd.deadline is not None
    assert tfd.created_at == todo_high_priority.created_at
    assert isinstance(tfd.created_at, datetime)
    assert tfd.idx == todo_high_priority.idx
    assert isinstance(tfd.idx, UUID)
