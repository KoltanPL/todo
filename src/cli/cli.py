from datetime import date

import typer
from rich.console import Console
from rich.table import Table

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo
from src.todo_list.todo_list import TodoList

app = typer.Typer(
    name='todo-app',
    help='A professional Todo CLI application'
)

console = Console()


@app.command()
def list_tasks():



    raw_tasks = [
        Todo('Improving Python', deadline=date(2027, 1, 2)),
        Todo('Learning Java', priority=PriorityEnum.HIGH),
        Todo('Clustering models'),
        Todo('SQL practice', tags=['SQL', 'Select', 'From'])
    ]
    tasks_list = TodoList(raw_tasks)



    if not len(tasks_list):
        console.print('[yellow]No tasks found.[/yellow]')
        return

    table = Table(title='Todo List', show_header=True, header_style='bold magenta')
    table.add_column('Status', justify='center')
    table.add_column('Priority', justify='center', width=8)
    table.add_column('Description', style='cyan')
    table.add_column('Deadline', justify='center')
    table.add_column('Tags', style='blue')
    table.add_column('Id', style='dim', no_wrap=True)

    status_icons = {
        StatusEnum.TODO: "🆕           ",
        StatusEnum.IN_PROGRESS: "🚧",
        StatusEnum.COMPLETED: "✅",
        StatusEnum.BLOCKED: "⛔",
    }

    priority_colors = {
        PriorityEnum.HIGH: "red",
        PriorityEnum.MEDIUM: "yellow",
        PriorityEnum.LOW: "green",
    }


    for task in tasks_list:
        status_icon = status_icons.get(task.status, "?")
        priority_color = priority_colors.get(task.priority, "white")
        priority_text = f"[{priority_color}]{task.priority.name}[/{priority_color}]"

        tags = ', '.join(task.tags) if task.tags else '-'

        table.add_row(
            status_icon.center(6),
            priority_text,
            task.description,
            str(task.deadline),
            tags,
            str(task.idx)
        )


    console.print(table)
