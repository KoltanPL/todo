from typing import TYPE_CHECKING

from src.cli.state import get_todo_list
from src.ui.console import console
from src.ui.tables import build_tasks_table


if TYPE_CHECKING:
    from rich.table import Table


def list_tasks() -> None:
    todo_list = get_todo_list()
    if not len(todo_list):
        console.print('[yellow]No tasks found.[/yellow]')
        return

    table: Table = build_tasks_table(todo_list)

    console.print(table)
