import typer

from src.cli.state import get_todo_list
from src.task.task import Todo
from src.ui.console import console
from src.ui.prompts import prompt_deadline_graphical, prompt_description, prompt_priority, prompt_status, prompt_tags


def add_task() -> None:
    description = prompt_description()

    priority = prompt_priority()
    status = prompt_status()

    try:
        deadline = prompt_deadline_graphical()
    except typer.Abort as err:
        console.print('[yellow]Operation cancelled.[/yellow]')
        raise typer.Exit() from err

    tags = prompt_tags()

    task = Todo(description=description, priority=priority, status=status, deadline=deadline, tags=tags)

    todo_list = get_todo_list()
    todo_list.add(task)

    console.print(f'[green]Added: [/green] {task.description} (id={(str(task.idx)[:8])})')
