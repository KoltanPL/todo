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


_todo_list = bootstrap_tasks()


def list_tasks() -> None:
    if not len(_todo_list):
        console.print('[yellow]No tasks found.[/yellow]')
        return

    table: Table = build_tasks_table(_todo_list)

    console.print(table)


def add_task(description: str = typer.Argument(..., help='Task description')) -> None:
    priority = prompt_priority()
    status = prompt_status()

    try:
        deadline = prompt_deadline_graphical()
    except typer.Abort() as err:
        console.print('[yellow]Operation cancelled.[/yellow]')
        raise typer.Exit() from err

    tags = prompt_tags()

    task = Todo(description=description, priority=priority, status=status, deadline=deadline, tags=tags)

    _todo_list.add(task)

    console.print(f'[green]Added: [/green] {task.description} (id={(str(task.idx)[:8])})')


def register_commands(app: Typer) -> None:
    app.command()(list_tasks)
    app.command()(add_task)
