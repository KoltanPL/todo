import pytest
import typer

from src.cli.commands.interactive import exit_app, interactive


def noop(*_: object, **__: object) -> None:
    return None


def test_exit_app(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    monkeypatch.setattr('src.cli.commands.interactive.console.print', fake_print)

    with pytest.raises(typer.Exit):
        exit_app()

    assert any('Bye' in str(call) for call in printed)


def test_interactive_calls_add_task(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, int] = {'add': 0}

    def fake_add() -> None:
        calls['add'] += 1
        raise typer.Exit()

    monkeypatch.setattr('src.cli.commands.interactive.add_task', fake_add)
    monkeypatch.setattr('src.cli.commands.interactive.list_tasks', noop)
    monkeypatch.setattr('src.cli.commands.interactive.update_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.remove_task', noop)

    def fake_menu(_: object) -> str:
        return 'Add task'

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_menu)

    with pytest.raises(typer.Exit):
        interactive()

    assert calls['add'] == 1


def test_interactive_calls_list_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, int] = {'list': 0}

    def fake_list() -> None:
        calls['list'] += 1
        raise typer.Exit()

    monkeypatch.setattr('src.cli.commands.interactive.add_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.list_tasks', fake_list)
    monkeypatch.setattr('src.cli.commands.interactive.update_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.remove_task', noop)

    def fake_menu(_: object) -> str:
        return 'Show tasks'

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_menu)

    with pytest.raises(typer.Exit):
        interactive()

    assert calls['list'] == 1


def test_interactive_calls_update_task(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, int] = {'update': 0}

    def fake_update() -> None:
        calls['update'] += 1
        raise typer.Exit()

    monkeypatch.setattr('src.cli.commands.interactive.add_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.list_tasks', noop)
    monkeypatch.setattr('src.cli.commands.interactive.update_task', fake_update)
    monkeypatch.setattr('src.cli.commands.interactive.remove_task', noop)

    def fake_menu(_: object) -> str:
        return 'Update task'

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_menu)

    with pytest.raises(typer.Exit):
        interactive()

    assert calls['update'] == 1


def test_interactive_calls_remove_task(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, int] = {'remove': 0}

    def fake_remove() -> None:
        calls['remove'] += 1
        raise typer.Exit()

    monkeypatch.setattr('src.cli.commands.interactive.add_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.list_tasks', noop)
    monkeypatch.setattr('src.cli.commands.interactive.update_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.remove_task', fake_remove)

    def fake_menu(_: object) -> str:
        return 'Remove task'

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_menu)

    with pytest.raises(typer.Exit):
        interactive()

    assert calls['remove'] == 1


def test_interactive_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr('src.cli.commands.interactive.add_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.list_tasks', noop)
    monkeypatch.setattr('src.cli.commands.interactive.update_task', noop)
    monkeypatch.setattr('src.cli.commands.interactive.remove_task', noop)

    def fake_menu(_: object) -> str:
        return 'Exit'

    monkeypatch.setattr('src.cli.commands.interactive.prompt_menu', fake_menu)

    with pytest.raises(typer.Exit):
        interactive()
