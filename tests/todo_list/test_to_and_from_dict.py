from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import src.todo_list.todo_list as todo_list_module
from src.todo_list.todo_list import TodoList


if TYPE_CHECKING:  # pragma: no cover
    from _pytest.monkeypatch import MonkeyPatch


@dataclass(frozen=True)
class _TodoStub:
    payload: dict[str, str]
    idx: UUID

    def to_dict(self) -> dict[str, str]:
        return self.payload

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> _TodoStub:
        return cls(payload=data, idx=uuid4())


def test_to_dict_builds_tasks_list(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(todo_list_module, 'Todo', _TodoStub, raising=True)

    todos = [_TodoStub({'description': 'a'}, uuid4()), _TodoStub({'description': 'b'}, uuid4())]

    my_todo_list = TodoList(todos)  # type: ignore[argtype]

    assert my_todo_list.to_dict() == {'tasks': [{'description': 'a'}, {'description': 'b'}]}


def test_from_dict_creates_todo_list_and_calls_todo_from_dict(monkeypatch: MonkeyPatch) -> None:
    calls: list[dict] = []

    class _TodoSpy(_TodoStub):
        @classmethod
        def from_dict(cls, data: dict[str, str]) -> _TodoSpy:
            calls.append(data)

            return cls(payload=data, idx=uuid4())

    monkeypatch.setattr(todo_list_module, 'Todo', _TodoSpy, raising=True)

    data = {'tasks': [{'description': 'a'}, {'description': 'b'}]}

    tl = TodoList.from_dict(data)  # type: ignore[argtype]

    assert isinstance(tl, TodoList)
    assert len(calls) == 2
    assert calls == [{'description': 'a'}, {'description': 'b'}]
