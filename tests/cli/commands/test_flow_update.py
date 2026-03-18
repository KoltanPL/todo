from datetime import date

import pytest
import typer

from src.cli.commands.flow_update import (
    BackToMenuError,
    move_back,
    update_description,
    update_priority,
    update_tags,
    update_task,
)
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


class DummyTodoList:
    def __init__(self, tasks: list[Todo]) -> None:
        self.tasks = tasks

    def __len__(self) -> int:
        return len(self.tasks)


def noop(*_: object, **__: object) -> None:
    return None


@pytest.fixture
def sample_task() -> Todo:
    """
    Provide a sample Todo object.

    Returns:
        Todo: Predefined task.
    """
    return Todo(
        description='Test',
        priority=PriorityEnum.HIGH,
        status=StatusEnum.TODO,
        deadline=None,
        tags=['x'],
    )


def test_update_task_invalid_id(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_prompt(_: str) -> str:
        return 'abc'

    monkeypatch.setattr('src.cli.commands.flow_update.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)

    update_task()

    assert any('Invalid task id.' in str(call) for call in printed)


def test_update_task_out_of_range(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_prompt(_: str) -> str:
        return '10'

    def fake_get() -> DummyTodoList:
        return DummyTodoList([])

    monkeypatch.setattr('src.cli.commands.flow_update.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.flow_update.get_todo_list', fake_get)

    update_task()

    assert any('out of range' in str(call) for call in printed)


def test_update_task_status_and_back(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    todo_list = DummyTodoList([sample_task])

    def fake_get() -> DummyTodoList:
        return todo_list

    def fake_prompt(_: str) -> str:
        return '1'

    actions = iter(['Status', 'Back'])

    def fake_menu(_: object) -> str:
        return next(actions)

    def fake_status() -> StatusEnum:
        return StatusEnum.COMPLETED

    saved: dict[str, bool] = {'called': False}

    def fake_save() -> None:
        saved['called'] = True

    monkeypatch.setattr('src.cli.commands.flow_update.get_todo_list', fake_get)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_menu', fake_menu)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_status', fake_status)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)
    monkeypatch.setattr('src.cli.commands.flow_update.console.clear', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.print_task_summary', lambda _: None)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.pause', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.save_todo_list', fake_save)

    update_task()

    assert sample_task.status == StatusEnum.COMPLETED
    assert saved['called'] is True


def test_update_task_back_immediately(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    todo_list = DummyTodoList([sample_task])

    def fake_get() -> DummyTodoList:
        return todo_list

    def fake_prompt(_: str) -> str:
        return '1'

    def fake_menu(_: object) -> str:
        return 'Back'

    saved: dict[str, bool] = {'called': False}

    def fake_save() -> None:
        saved['called'] = True

    monkeypatch.setattr('src.cli.commands.flow_update.get_todo_list', fake_get)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_menu', fake_menu)
    monkeypatch.setattr('src.cli.commands.flow_update.console.clear', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.print_task_summary', lambda _: None)
    monkeypatch.setattr('src.cli.commands.flow_update.save_todo_list', fake_save)

    update_task()

    assert saved['called'] is True


def test_update_task_deadline_abort(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    todo_list = DummyTodoList([sample_task])

    def fake_get() -> DummyTodoList:
        return todo_list

    def fake_prompt(_: str) -> str:
        return '1'

    actions = iter(['Deadline', 'Back'])

    def fake_menu(_: object) -> str:
        return next(actions)

    def fake_deadline() -> None:
        raise typer.Abort()

    monkeypatch.setattr('src.cli.commands.flow_update.get_todo_list', fake_get)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_menu', fake_menu)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_deadline_graphical', fake_deadline)
    monkeypatch.setattr('src.cli.commands.flow_update.console.clear', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.print_task_summary', lambda _: None)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.pause', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.save_todo_list', lambda: None)

    update_task()


def test_update_priority(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    def fake_priority() -> PriorityEnum:
        return PriorityEnum.LOW

    monkeypatch.setattr('src.cli.commands.flow_update.prompt_priority', fake_priority)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)

    update_priority(sample_task)

    assert sample_task.priority == PriorityEnum.LOW


def test_update_description(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    def fake_desc() -> str:
        return 'Updated'

    monkeypatch.setattr('src.cli.commands.flow_update.prompt_description', fake_desc)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)

    update_description(sample_task)

    assert sample_task.description == 'Updated'


def test_update_tags(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    def fake_tags() -> list[str]:
        return ['a', 'b']

    monkeypatch.setattr('src.cli.commands.flow_update.prompt_tags', fake_tags)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)

    update_tags(sample_task)

    assert sample_task.tags == ['a', 'b']


def test_update_tags_empty(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    def fake_tags() -> list[str]:
        return []

    monkeypatch.setattr('src.cli.commands.flow_update.prompt_tags', fake_tags)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)

    update_tags(sample_task)

    assert sample_task.tags == []


def test_move_back_raises() -> None:
    with pytest.raises(BackToMenuError):
        move_back(None)  # type: ignore[arg-type]


def test_update_task_deadline_success(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    todo_list = DummyTodoList([sample_task])

    def fake_get() -> DummyTodoList:
        return todo_list

    def fake_prompt(_: str) -> str:
        return '1'

    actions = iter(['Deadline', 'Back'])

    def fake_menu(_: object) -> str:
        return next(actions)

    def fake_deadline() -> date:
        return date(2027, 1, 1)

    monkeypatch.setattr('src.cli.commands.flow_update.get_todo_list', fake_get)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_menu', fake_menu)
    monkeypatch.setattr('src.cli.commands.flow_update.prompt_deadline_graphical', fake_deadline)
    monkeypatch.setattr('src.cli.commands.flow_update.console.clear', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.print_task_summary', lambda _: None)
    monkeypatch.setattr('src.cli.commands.flow_update.console.print', noop)
    monkeypatch.setattr('src.cli.commands.flow_update.typer.pause', lambda: None)
    monkeypatch.setattr('src.cli.commands.flow_update.save_todo_list', lambda: None)

    update_task()

    assert sample_task.deadline == date(2027, 1, 1)
