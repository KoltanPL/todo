from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

import pytest

import src.todo_list.todo_list as todo_list_module


if TYPE_CHECKING:
    from types import ModuleType

    from _pytest.monkeypatch import MonkeyPatch


@dataclass(frozen=True)
class _TodoStub:
    idx: UUID
    description: str
    tags: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {'idx': str(self.idx), 'description': self.description, 'tags': self.tags}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> _TodoStub:
        return cls(idx=UUID(data['idx']), description=data['description'], tags=data['tags'])


@pytest.fixture
def todos() -> list[_TodoStub]:
    return [
        _TodoStub(idx=uuid4(), description='Python', tags=['Python', 'SQL']),
        _TodoStub(idx=uuid4(), description='Zażółć gęślą jaźń', tags=['Polski', 'Unicode']),
    ]


@pytest.fixture
def patch_dependencies(monkeypatch: MonkeyPatch) -> ModuleType:
    monkeypatch.setattr(todo_list_module, 'Todo', _TodoStub, raising=True)

    return todo_list_module
