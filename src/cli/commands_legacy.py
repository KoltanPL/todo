from collections.abc import Callable
from enum import StrEnum
from typing import TYPE_CHECKING

import typer
from typer import Typer

from src.bootstrap import bootstrap_tasks
from src.cli.cli import console
from src.task.task import Todo
from src.ui.prompts import prompt_deadline_graphical, prompt_priority, prompt_status, prompt_tags
from src.ui.tables import build_tasks_table

if TYPE_CHECKING:
    from rich.table import Table


class UpdateFieldAction(StrEnum):
    STATUS = '1'
    PRIORITY = '2'
    DESCRIPTION = '3'
    DEADLINE = '4'
    TAGS = '5'
    BACK = '6'


def prompt_update_field() -> UpdateFieldAction:
    console.print('\n[bold]Update field[/bold]')
    console.print(' [cyan]1[/cyan] Status')
    console.print(' [cyan]2[/cyan] Priority')
    console.print(' [cyan]3[/cyan] Description')
    console.print(' [cyan]4[/cyan] Deadline')
    console.print(' [cyan]5[/cyan] Tags')
    console.print(' [cyan]6[/cyan] Back')

    def _coerce(raw: str) -> UpdateFieldAction:
        try:
            return UpdateFieldAction(raw.strip())
        except ValueError:
            raise typer.BadParameter('Choose 1-6')

    return typer.prompt('Choose', value_proc=_coerce)


def print_task_summary(task: Todo, highlight_field: str | None = None) -> None:
    from rich.table import Table
    from rich import box

    console.print()

    table = Table(title='Current Task', box=box.ROUNDED, show_header=False)
    table.add_column('Field', style='bold cyan')
    table.add_column('Value')

    def style(field: str, value: str) -> str:
        if highlight_field == field:
            return f'[bold green]{value}[/bold green]'
        return value

    table.add_row('Status', style('status', task.status.value))
    table.add_row('Priority', style('priority', task.priority.name))
    table.add_row('Description', style('description', task.description))
    table.add_row('Deadline', style('deadline', str(task.deadline)))
    table.add_row('Tags', style('tags', ', '.join(task.tags) if task.tags else '-'))

    console.print(table)


def update_status(task: Todo) -> None:
    task.status = prompt_status()
    console.print(f'[green]Status updated:[/green] {task.status.value}')


def update_priority(task: Todo) -> None:
    task.priority = prompt_priority()
    console.print(f'[green]Priority updated:[/green] {task.priority.name}')


def update_description(task: Todo) -> None:
    new_desc = typer.prompt('New description').strip()
    if not new_desc:
        console.print('[red]Description cannot be empty.[/red]')
        return

    task.description = new_desc
    console.print(f'[green]Description updated:[/green] {task.description}')


def update_deadline(task: Todo) -> None:
    try:
        task.deadline = prompt_deadline_graphical()
    except typer.Abort:
        return

    console.print(f'[green]Deadline updated:[/green] {task.deadline}')


def update_tags(task: Todo) -> None:
    task.tags = prompt_tags()
    console.print(
        f'[green]Tags updated:[/green] {", ".join(task.tags) if task.tags else "-"}'
    )


def update_task() -> None:
    raw_id = typer.prompt('Task id').strip()

    try:
        parsed_id = int(raw_id) - 1
    except ValueError:
        console.print('[red]Invalid task id.[/red]')
        return

    if not (0 <= parsed_id < len(_todo_list)):
        console.print('[red]Provided id is out of range.[/red]')
        return

    task = _todo_list.tasks[parsed_id]

    update_handlers: dict[UpdateFieldAction, Callable[[Todo], None]] = {
        UpdateFieldAction.STATUS: update_status,
        UpdateFieldAction.PRIORITY: update_priority,
        UpdateFieldAction.DESCRIPTION: update_description,
        UpdateFieldAction.DEADLINE: update_deadline,
        UpdateFieldAction.TAGS: update_tags,
    }

    while True:
        console.clear()
        print_task_summary(task)

        action = prompt_update_field()

        if action is UpdateFieldAction.BACK:
            console.clear()
            return

        handler = update_handlers.get(action)
        if handler:
            console.clear()
            handler(task)
            console.print('\n[green]Updated successfully.[/green]')
            typer.pause()
