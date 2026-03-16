import typer

from src.cli.state import get_todo_list, save_todo_list
from src.ui.console import console


def remove_task() -> None:
    raw_id = typer.prompt('Task id').strip()

    try:
        parsed_id = int(raw_id) - 1
    except ValueError:
        console.print('[red]Invalid task id.[/red]')
        return

    todo_list = get_todo_list()

    if not (0 <= parsed_id < len(todo_list)):
        console.print('[red]Provided id is out of range.[/red]')
        return

    task = todo_list.tasks[parsed_id]
    todo_list.remove(task.idx)
    save_todo_list()

    console.print(f'[green]Task removed:[/green] {task.description}')
