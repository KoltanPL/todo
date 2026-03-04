from collections.abc import Callable
from enum import StrEnum

import typer

from src.cli.commands.add_task import add_task
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task
from src.ui.console import console


class MenuAction(StrEnum):
    ADD = '1'
    LIST = '2'
    REMOVE = '3'
    EXIT = '4'


def prompt_action() -> MenuAction:
    console.print('\n[bold]Menu[/bold]')
    console.print('  [cyan]1[/cyan] Add task')
    console.print('  [cyan]2[/cyan] Show tasks')
    console.print('  [cyan]3[/cyan] Remove task')
    console.print('  [cyan]4[/cyan] Exit')

    def _coerce(raw: str) -> MenuAction:
        try:
            return MenuAction(raw.strip())
        except ValueError:
            raise typer.BadParameter('Choose 1-5')

    return typer.prompt('Choose', default=MenuAction.LIST.value, value_proc=_coerce)


def interactive() -> None:
    handlers: dict[MenuAction, Callable[[], None]] = {
        MenuAction.ADD: add_task,
        MenuAction.LIST: list_tasks,
        MenuAction.REMOVE: remove_task,
    }

    while True:
        action = prompt_action()

        if action is MenuAction.EXIT:
            console.print('[dim]Bye 👋[/dim]')
            raise typer.Exit()

        handlers[action]()
