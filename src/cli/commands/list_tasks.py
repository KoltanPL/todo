from rich.table import Table

from src.cli.cli import console
from src.cli.state import get_todo_list
from src.ui.tables import build_tasks_table


def list_tasks() -> None:
    todo_list = get_todo_list()
    if not len(todo_list):
        console.print('[yellow]No tasks found.[/yellow]')
        return

    table: Table = build_tasks_table(todo_list)

    console.print(table)
