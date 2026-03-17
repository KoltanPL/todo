from typing import TYPE_CHECKING

import pytest
import typer

from src.cli.commands.add_task import add_task
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


if TYPE_CHECKING:
    from src.task.task import Todo


class DummyTodoList:
    """
    Simple stub for TodoList.
    """

    def __init__(self) -> None:
        self.tasks: list[Todo] = []

    def add(self, task: Todo) -> None:
        self.tasks.append(task)


@pytest.fixture
def dummy_todo_list() -> DummyTodoList:
    """
    Provide a dummy TodoList instance.

    Returns:
        DummyTodoList: Empty task container.
    """
    return DummyTodoList()


def test_add_task_happy_path(monkeypatch: pytest.MonkeyPatch, dummy_todo_list: DummyTodoList) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_prompt_description() -> str:
        return 'Test task'

    def fake_prompt_priority() -> PriorityEnum:
        return PriorityEnum.HIGH

    def fake_prompt_status() -> StatusEnum:
        return StatusEnum.TODO

    def fake_prompt_deadline() -> None:
        return None

    def fake_prompt_tags() -> list[str]:
        return ['python']

    def fake_get_todo_list() -> DummyTodoList:
        return dummy_todo_list

    saved: dict[str, bool] = {'called': False}

    def fake_save() -> None:
        saved['called'] = True

    monkeypatch.setattr('src.cli.commands.add_task.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_description', fake_prompt_description)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_priority', fake_prompt_priority)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_status', fake_prompt_status)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_deadline_graphical', fake_prompt_deadline)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_tags', fake_prompt_tags)
    monkeypatch.setattr('src.cli.commands.add_task.get_todo_list', fake_get_todo_list)
    monkeypatch.setattr('src.cli.commands.add_task.save_todo_list', fake_save)

    add_task()

    assert len(dummy_todo_list.tasks) == 1
    task = dummy_todo_list.tasks[0]

    assert task.description == 'Test task'
    assert task.priority == PriorityEnum.HIGH
    assert task.status == StatusEnum.TODO
    assert task.deadline is None
    assert task.tags == ['python']

    assert saved['called'] is True

    assert any('Added:' in str(call) for call in printed)


def test_add_task_abort_on_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_prompt_description() -> str:
        return 'Test task'

    def fake_prompt_priority() -> PriorityEnum:
        return PriorityEnum.HIGH

    def fake_prompt_status() -> StatusEnum:
        return StatusEnum.TODO

    def fake_prompt_deadline() -> None:
        raise typer.Abort()

    def fake_print(*args: object, **kwargs: object) -> None:
        pass

    monkeypatch.setattr('src.cli.commands.add_task.prompt_description', fake_prompt_description)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_priority', fake_prompt_priority)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_status', fake_prompt_status)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_deadline_graphical', fake_prompt_deadline)
    monkeypatch.setattr('src.cli.commands.add_task.console.print', fake_print)

    with pytest.raises(typer.Exit):
        add_task()
