from typing import TYPE_CHECKING

from rich import box
from rich.table import Table

from src.ui.console import console


if TYPE_CHECKING:
    from src.task.task import Todo  # pragma: no cover


def print_task_summary(task: Todo, highlight_field: str | None = None) -> None:
    """Display a summary of a single task in a formatted table.

    Renders task details such as status, priority, description, deadline,
    and tags using a rich table. Optionally highlights a selected field.

    Args:
        task (Todo): Task to display.
        highlight_field (str | None): Name of the field to highlight
            (e.g. "status", "priority"). If None, no field is highlighted.
    """
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
