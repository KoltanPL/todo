from collections.abc import Callable
from datetime import date, timedelta
from enum import StrEnum
from uuid import UUID

from rich import box
from rich.console import Console
from rich.table import Table
import typer
from simple_term_menu import TerminalMenu

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo
from src.todo_list.todo_list import TodoList

app = typer.Typer(name='todo-app', help='A professional Todo CLI application')

console = Console()

raw_tasks = [
    Todo('Improving Python', deadline=date(2027, 1, 2)),
    Todo('Learning Java', priority=PriorityEnum.HIGH),
    Todo('Clustering models'),
    Todo('SQL practice', tags=['SQL', 'Select', 'From']),
]
tasks_list = TodoList(raw_tasks)


@app.command()
def add_task(description: str = typer.Argument(..., help='Task description')):
    task = Todo(description=description)

    tasks_list.add(task)

    console.print(f'[green]Added: [/green] {task.description} (id={(str(task.idx)[:8])})')


@app.command()
def list_tasks():
    if not len(tasks_list):
        console.print('[yellow]No tasks found.[/yellow]')
        return

    table = Table(title='Todo List', show_header=True, header_style='bold magenta', box=box.SIMPLE)
    table.add_column('Id', style='dim', no_wrap=True)
    table.add_column('Status', justify='center')
    table.add_column('Priority', justify='center', width=8)
    table.add_column('Description', style='cyan')
    table.add_column('Deadline', justify='center')
    table.add_column('Tags', style='blue')

    priority_colors = {
        PriorityEnum.HIGH: 'red',
        PriorityEnum.MEDIUM: 'yellow',
        PriorityEnum.LOW: 'green',
    }

    for idx, task in enumerate(tasks_list, 1):
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

    console.print(table)


def prompt_deadline_graphical() -> date | None:
    options = [
        'No deadline',
        'Today',
        'Tomorrow',
        'In 7 days',
        'In 14 days',
        'Pick exact date (YYYY-MM-DD)',
    ]
    idx = TerminalMenu(options).show()
    if idx is None:
        raise typer.Abort()

    if idx == 0:
        return None
    if idx == 1:
        return date.today()
    if idx == 2:
        return date.today() + timedelta(days=1)
    if idx == 3:
        return date.today() + timedelta(days=7)
    if idx == 4:
        return date.today() + timedelta(days=14)
    while True:
        raw = typer.prompt('Deadline (YYYY-MM-DD)').strip()

        try:
            user_deadline = date.fromisoformat(raw)
            if user_deadline > date.today():
                return user_deadline
            else:
                typer.echo('Date should be in the future.')
        except ValueError:
            typer.echo('Invalid date. Example: 2026-03-01')


def handle_add():
    desc = typer.prompt('Task description').strip()

    if not desc:
        console.print('[yellow]Description cannot be empty.[/yellow]')
        return

    console.print('\n[bold]Choose priority:[/bold]')
    priority_options = [p.name.title() for p in PriorityEnum]
    priority_menu = TerminalMenu(priority_options)
    chosen_priority = priority_options[priority_menu.show()]
    priority = PriorityEnum[chosen_priority.upper()]

    console.print('\n[bold]Choose status:[/bold]')
    status_options = [s.value for s in StatusEnum]
    status_menu = TerminalMenu(status_options)
    chosen_status = status_options[status_menu.show()]
    status = StatusEnum(chosen_status)

    deadline = prompt_deadline_graphical()

    tags = typer.prompt('Task tags(comma separated)').split(',')

    task = Todo(desc, priority, deadline=deadline, status=status, tags=tags)
    tasks_list.add(task)
    console.print(f'[green]Added: [/green] {task.description} (id={(str(task.idx)[:8])})')


def print_task_summary(task: Todo, highlight_field: str | None = None) -> None:
    console.print()

    table = Table(title='Current Task', box=box.ROUNDED, show_header=False)

    table.add_column('Field', style='bold cyan')
    table.add_column('Value')

    def style(field_name: str, value: str) -> str:
        if highlight_field == field_name:
            return f'[bold green]{value}[/bold green]'
        return value

    table.add_row('Status', style('status', task.status.value))
    table.add_row('Priority', style('priority', task.priority.name))
    table.add_row('Description', style('description', task.description))
    table.add_row('Deadline', style('deadline', str(task.deadline)))
    table.add_row('Tags', style('tags', ', '.join(task.tags) if task.tags else '-'))

    console.print(table)


def handle_update() -> None:
    raw_id = typer.prompt('Task id ').strip()

    try:
        parsed_id = int(raw_id) - 1
    except ValueError:
        console.print('[red]Invalid task id.[/red]')
        return

    if not (0 <= parsed_id < len(tasks_list)):
        console.print('[red]Provided id is out of range.[/red]')
        return

    task = tasks_list.tasks[parsed_id]

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

            field_map = {
                UpdateFieldAction.STATUS: 'status',
                UpdateFieldAction.PRIORITY: 'priority',
                UpdateFieldAction.DESCRIPTION: 'description',
                UpdateFieldAction.DEADLINE: 'deadline',
                UpdateFieldAction.TAGS: 'tags',
            }

            changed_field = field_map.get(action)

            console.print('\n[green]Updated successfully.[/green]')
            print_task_summary(task, highlight_field=changed_field)

            typer.pause()


def handle_remove() -> None:
    raw_id = typer.prompt('Task id ').strip()

    try:
        parsed_id = int(raw_id) - 1
    except ValueError:
        console.print('[red]Invalid task id.[/red]')
        return

    if not (0 <= parsed_id < len(tasks_list)):
        console.print('[red]Provided id is out of range.[/red]')
        return

    task_to_remove = tasks_list.tasks[parsed_id]

    tasks_list.remove(task_to_remove.idx)
    console.print(f'[green]Task removed: [/green] {task_to_remove.description}')


def update_description(task: Todo) -> None:
    new_description = typer.prompt('Enter a new description').title()
    old_description = task.description

    try:
        task.description = new_description
    except ValueError as e:
        console.print(f'[red]{e}[/red]')
        console.print(f'[yellow]Description remains:[/yellow] {old_description}')
        return

    console.print(f'[green]Description updated to:[/green] {task.description}')


def update_status(task: Todo) -> None:
    options = [s.value for s in StatusEnum]
    idx = TerminalMenu(options).show()

    if idx is None:
        return

    task.status = StatusEnum(options[idx])
    console.print(f'[green]Status updated to:[/green] {task.status.value}')


def update_priority(task: Todo) -> None:
    options = [p.name.title() for p in PriorityEnum]
    idx = TerminalMenu(options).show()

    if idx is None:
        return

    task.priority = PriorityEnum[options[idx].upper()]
    console.print(f'[green]Priority updated to:[/green] {task.priority.name}')


def update_deadline(task: Todo) -> None:
    try:
        new_deadline = prompt_deadline_graphical()
    except typer.Abort:
        return

    task.deadline = new_deadline
    console.print(f'[green]Deadline updated to:[/green] {task.deadline}')


def update_tags(task: Todo) -> None:
    raw = typer.prompt('Enter tags (comma separated)')
    tags = [t.strip() for t in raw.split(',') if t.strip()]
    task.tags = tags
    console.print(f'[green]Tags updated to:[/green] {", ".join(task.tags) if task.tags else "-"}')


class UpdateFieldAction(StrEnum):
    STATUS = '1'
    PRIORITY = '2'
    DESCRIPTION = '3'
    DEADLINE = '4'
    TAGS = '5'
    BACK = '6'


def prompt_update_field() -> UpdateFieldAction:
    console.print('\n[bold]Update field[/bold]')
    console.print(' [cyan]1[cyan] Status')
    console.print(' [cyan]2[cyan] Priority')
    console.print(' [cyan]3[cyan] Description')
    console.print(' [cyan]4[cyan] Deadline')
    console.print(' [cyan]5[cyan] Tags')
    console.print(' [cyan]6[cyan] Back')

    def _coerce(raw: str) -> UpdateFieldAction:
        raw = raw.strip()
        try:
            return UpdateFieldAction(raw)
        except ValueError:
            raise typer.BadParameter('Choose 1-6')

    return typer.prompt('Choose', value_proc=_coerce)


class MenuAction(StrEnum):
    ADD = '1'
    LIST = '2'
    REMOVE = '3'
    UPDATE = '4'
    EXIT = '5'


def prompt_action() -> MenuAction:
    console.print('\n[bold]Menu[/bold]')
    console.print('  [cyan]1[/cyan] Add task')
    console.print('  [cyan]2[/cyan] Show tasks')
    console.print('  [cyan]3[/cyan] Remove task')
    console.print('  [cyan]4[/cyan] Update')
    console.print('  [cyan]5[/cyan] Exit')

    def _coerce(raw: str) -> MenuAction:
        raw = raw.strip()
        try:
            return MenuAction(raw)
        except ValueError:
            raise typer.BadParameter('Choose 1, 2, 3, 4, 5.')

    return typer.prompt('Choose', default=MenuAction.LIST.value, value_proc=_coerce)


@app.command()
def interactive():
    handlers: dict[MenuAction, Callable[[], None]] = {
        MenuAction.ADD: handle_add,
        MenuAction.LIST: list_tasks,
        MenuAction.UPDATE: handle_update,
        MenuAction.REMOVE: handle_remove,
    }

    while True:
        action = prompt_action()
        if action is MenuAction.EXIT:
            console.print('[dim]Bye 👋[/dim]')
            raise typer.Exit(code=0)
        handlers[action]()
