from typing import TYPE_CHECKING

from rich import box
from rich.table import Table

from src.enums.priority_enum import PriorityEnum


if TYPE_CHECKING:
    from src.todo_list.todo_list import TodoList  # pragma: no cover


def build_tasks_table(tasks: TodoList) -> Table:
    """Build a formatted table representation of tasks.

    Creates a rich table displaying task attributes such as status,
    priority, description, deadline, and tags. Priority values are
    color-coded for better readability.

    Args:
        tasks (TodoList): Collection of tasks to display.

    Returns:
        Table: Renderable rich table with task data.
    """
    table = Table(title='Todo List', show_header=True, header_style='bold magenta', box=box.SIMPLE)

    table.add_column('Id', style='dim', no_wrap=True)
    table.add_column('Status', justify='center')
    table.add_column('Priority', justify='center', width=8)
    table.add_column('Description', style='cyan')
    table.add_column('Deadline', justify='center')
    table.add_column('Tags', style='blue')

    priority_colors: dict[PriorityEnum, str] = {
        PriorityEnum.HIGH: 'red',
        PriorityEnum.MEDIUM: 'yellow',
        PriorityEnum.LOW: 'green',
    }

    for idx, task in enumerate(tasks, 1):
        status_icon = task.status.value
        priority_color = priority_colors.get(task.priority, 'white')
        priority_text = f'[{priority_color}]{task.priority.name}[/{priority_color}]'

        tags = ', '.join(task.tags) if task.tags else '-'

        table.add_row(
            str(idx),
            status_icon.center(6),
            priority_text,
            task.description,
            str(task.deadline),
            tags,
        )

    return table
