from typing import TYPE_CHECKING, cast

from src.cli.commands.add_task import add_task
from src.cli.commands.flow_update import update_task
from src.cli.commands.interactive import interactive
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task
from src.cli.registry import register_commands


if TYPE_CHECKING:
    from collections.abc import Callable

    from typer import Typer


class DummyApp:
    def __init__(self) -> None:
        self.commands: list[Callable[..., object]] = []

    def command(self) -> Callable[[Callable[..., object]], Callable[..., object]]:
        def decorator(func: Callable[..., object]) -> Callable[..., object]:
            self.commands.append(func)
            return func

        return decorator


def test_register_commands() -> None:
    app = DummyApp()

    register_commands(cast('Typer', app))

    assert app.commands == [
        list_tasks,
        add_task,
        remove_task,
        interactive,
        update_task,
    ]
