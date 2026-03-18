from typing import TYPE_CHECKING

from rich import box
from rich.table import Table

from src.ui.console import console


if TYPE_CHECKING:
    from src.task.task import Todo  # pragma: no cover


def print_task_summary(task: Todo, highlight_field: str | None = None) -> None:
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
