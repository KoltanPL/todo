from typing import TYPE_CHECKING

import typer
from typer.testing import CliRunner

from src.cli.registry import register_commands
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


if TYPE_CHECKING:
    import pytest


class DummyTodoList:
    def __init__(self) -> None:
        self.tasks: list[object] = []
        self.removed: list[object] = []

    def __len__(self) -> int:
        return len(self.tasks)

    def add(self, task: object) -> None:
        self.tasks.append(task)

    def remove(self, idx: object) -> None:
        self.removed.append(idx)


def build_app() -> typer.Typer:
    app = typer.Typer(name='todo-app', help='A professional Todo CLI application')
    register_commands(app)
    return app


def test_cli_help_lists_registered_commands() -> None:
    runner = CliRunner()

    result = runner.invoke(build_app(), ['--help'], color=False)

    assert result.exit_code == 0
    assert 'list-tasks' in result.stdout
    assert 'add-task' in result.stdout
    assert 'remove-task' in result.stdout
    assert 'interactive' in result.stdout
    assert 'update-task' in result.stdout


def test_add_task_command_runs_via_typer(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    todo_list = DummyTodoList()
    saved = {'called': False}

    def fake_save() -> None:
        saved['called'] = True

    monkeypatch.setattr('src.cli.commands.add_task.prompt_description', lambda: 'CLI task')
    monkeypatch.setattr('src.cli.commands.add_task.prompt_priority', lambda: PriorityEnum.HIGH)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_status', lambda: StatusEnum.TODO)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_deadline_graphical', lambda: None)
    monkeypatch.setattr('src.cli.commands.add_task.prompt_tags', lambda: ['cli'])
    monkeypatch.setattr('src.cli.commands.add_task.get_todo_list', lambda: todo_list)
    monkeypatch.setattr('src.cli.commands.add_task.save_todo_list', fake_save())

    result = runner.invoke(build_app(), ['add-task'], color=False)

    assert result.exit_code == 1
    assert len(todo_list.tasks) == 1
    assert saved['called'] is True


def test_remove_task_invalid_id_runs_via_typer() -> None:
    runner = CliRunner()

    result = runner.invoke(build_app(), ['remove-task'], input='abc\n', color=False)

    assert result.exit_code == 0
    assert 'Task id' in result.stdout
    assert 'Invalid task id.' in result.stdout


def test_interactive_exit_runs_via_typer(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    calls = {'menu': 0, 'exit': 0}

    def fake_prompt_menu(_: object) -> str:
        calls['menu'] += 1
        return 'Exit'

    def fake_exit_app() -> None:
        calls['exit'] += 1
        raise typer.Exit()

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_prompt_menu)
    monkeypatch.setattr('src.cli.commands.interactive.exit_app', fake_exit_app)

    result = runner.invoke(build_app(), ['interactive'], color=False)

    assert result.exit_code == 0
    assert calls == {'menu': 1, 'exit': 1}
