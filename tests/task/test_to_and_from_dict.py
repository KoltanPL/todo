import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


if TYPE_CHECKING:  # pragma: no cover
    from src.schemas.todo_schema import TodoDict


def test_to_dict_correct(todo_high_priority: Todo) -> None:
    mtd = todo_high_priority.to_dict()

    assert mtd['description'] == 'Learn FastAPI'
    assert mtd['priority'] == 3
    assert mtd['tags'] == ['urgent', 'backend']
    assert mtd['status'] == 'todo'
    assert mtd['created_at'] == '2025-12-11T21:30:00+00:00'
    assert mtd['deadline'] == '2025-12-13'
    assert mtd['idx'] == '7f4deca0-44b7-413a-80d7-550fedb1dc6a'


def test_from_dict_correct() -> None:
    mtd: TodoDict = {
        'description': 'Learn FastAPI',
        'priority': 3,
        'created_at': '2026-01-14T19:52:00.737625+00:00',
        'deadline': '2026-01-16',
        'tags': ['urgent', 'backend'],
        'status': 'todo',
        'idx': '7f4deca0-44b7-413a-80d7-550fedb1dc6a',
    }

    tfd = Todo.from_dict(mtd)

    assert isinstance(tfd, Todo)
    assert tfd.description == 'Learn FastAPI'
    assert tfd.priority == PriorityEnum.HIGH
    assert tfd.status == StatusEnum.TODO
    assert tfd.tags == ['urgent', 'backend']
    assert tfd.deadline == datetime.date(2026, 1, 16)
    assert tfd.created_at == datetime.datetime(2026, 1, 14, 19, 52, 0, 737625, tzinfo=datetime.UTC)
    assert tfd.idx == UUID('7f4deca0-44b7-413a-80d7-550fedb1dc6a')
