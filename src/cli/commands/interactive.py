from typing import TYPE_CHECKING, Never

import typer

from src.cli.commands.add_task import add_task
from src.cli.commands.flow_update import update_task
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task
from src.ui.console import console
from src.ui.prompts import prompt_menu


if TYPE_CHECKING:
    from collections.abc import Callable  # pragma: no cover


def exit_app() -> Never:
    console.print('[dim]Bye 👋[/dim]')
    raise typer.Exit()


def interactive() -> None:
    handlers: dict[str, Callable[[], None]] = {
        'Add task': add_task,
        'Show tasks': list_tasks,
        'Update task': update_task,
        'Remove task': remove_task,
        'Exit': exit_app,
    }

    while True:
        action = prompt_menu(handlers.keys())

        handlers[action]()
