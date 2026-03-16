from typing import TYPE_CHECKING

import typer

from src.cli.commands.print_task_summary import print_task_summary
from src.cli.state import get_todo_list, save_todo_list
from src.ui.console import console
from src.ui.prompts import (
    prompt_deadline_graphical,
    prompt_description,
    prompt_menu,
    prompt_priority,
    prompt_status,
    prompt_tags,
)


if TYPE_CHECKING:
    from collections.abc import Callable

    from src.task.task import Todo


class BackToMenuError(Exception):
    pass


def move_back(_task: Todo) -> None:
    raise BackToMenuError()


def update_status(task: Todo) -> None:
    task.status = prompt_status()
    console.print(f'[green]Status updated:[/green] {task.status.value}')


def update_priority(task: Todo) -> None:
    task.priority = prompt_priority()
    console.print(f'[green]Priority updated:[/green] {task.priority.name}')


def update_description(task: Todo) -> None:
    task.description = prompt_description()
    console.print(f'[green]Description updated:[/green] {task.description}')


def update_deadline(task: Todo) -> None:
    try:
        task.deadline = prompt_deadline_graphical()
    except typer.Abort:
        return

    console.print(f'[green]Deadline updated:[/green] {task.deadline}')


def update_tags(task: Todo) -> None:
    task.tags = prompt_tags()
    console.print(f'[green]Tags updated:[/green] {", ".join(task.tags) if task.tags else "-"}')


def update_task() -> None:
    todo_list = get_todo_list()
    raw_id = typer.prompt('Task id').strip()

    try:
        parsed_id = int(raw_id) - 1
    except ValueError:
        console.print('[red]Invalid task id.[/red]')
        return

    if not (0 <= parsed_id < len(todo_list)):
        console.print('[red]Provided id is out of range.[/red]')
        return

    task = todo_list.tasks[parsed_id]

    update_handlers: dict[str, Callable[[Todo], None]] = {
        'Status': update_status,
        'Priority': update_priority,
        'Description': update_description,
        'Deadline': update_deadline,
        'Tags': update_tags,
        'Back': move_back,
    }

    while True:
        console.clear()
        print_task_summary(task)

        action = prompt_menu(update_handlers.keys())
        handler = update_handlers[action]

        try:
            console.clear()
            handler(task)
            console.print('\n[green]Updated successfully.[/green]')
            typer.pause()

        except BackToMenuError:
            save_todo_list()
            return
