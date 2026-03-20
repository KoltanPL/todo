from typing import TYPE_CHECKING

import typer

from src.cli.commands.print_task_summary import print_task_summary
from src.cli.state import get_todo_list, save_todo_list
from src.ui.console import console
from src.ui.prompts import (
    prompt_deadline_graphical,
    prompt_description,
    prompt_menu,
    prompt_priority,
    prompt_status,
    prompt_tags,
)


if TYPE_CHECKING:
    from collections.abc import Callable  # pragma: no cover

    from src.task.task import Todo  # pragma: no cover


class BackToMenuError(Exception):
    """Exception used to signal returning to the main menu."""


class UpdateCancelledError(Exception):
    """Exception used to signal a cancelled field update."""


def move_back(_task: Todo) -> None:
    """Raise an exception to exit the update flow and return to menu.

    Args:
        _task (Todo): Ignored task instance (required for handler signature).

    Raises:
        BackToMenuError: Always raised to break the update loop.
    """
    raise BackToMenuError()


def update_status(task: Todo) -> None:
    """Update the status of a task.

    Prompts the user for a new status and assigns it to the task.

    Args:
        task (Todo): Task to update.
    """
    task.status = prompt_status()
    console.print(f'[green]Status updated:[/green] {task.status.value}')


def update_priority(task: Todo) -> None:
    """Update the priority of a task.

    Prompts the user for a new priority and assigns it to the task.

    Args:
        task (Todo): Task to update.
    """
    task.priority = prompt_priority()
    console.print(f'[green]Priority updated:[/green] {task.priority.name}')


def update_description(task: Todo) -> None:
    """Update the description of a task.

    Prompts the user for a new description and assigns it to the task.

    Args:
        task (Todo): Task to update.
    """
    task.description = prompt_description()
    console.print(f'[green]Description updated:[/green] {task.description}')


def update_deadline(task: Todo) -> None:
    """Update the deadline of a task.

    Prompts the user for a new deadline. If the operation is aborted,
    the deadline remains unchanged.

    Args:
        task (Todo): Task to update.
    """
    try:
        task.deadline = prompt_deadline_graphical()
    except typer.Abort as err:
        raise UpdateCancelledError() from err

    console.print(f'[green]Deadline updated:[/green] {task.deadline}')


def update_tags(task: Todo) -> None:
    """Update the tags of a task.

    Prompts the user for a list of tags and assigns them to the task.

    Args:
        task (Todo): Task to update.
    """
    task.tags = prompt_tags()
    console.print(f'[green]Tags updated:[/green] {", ".join(task.tags) if task.tags else "-"}')


def update_task() -> None:
    """Interactive flow for updating a selected task.

    Prompts the user for a task ID, validates it, and allows iterative updates
    of different task fields (status, priority, description, deadline, tags).
    The user can exit the update loop by selecting the "Back" option.

    Raises:
        typer.Exit: If user aborts input (indirectly via sub-prompts).
    """
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

    update_handlers: dict[str, Callable[[Todo], None]] = {
        'Status': update_status,
        'Priority': update_priority,
        'Description': update_description,
        'Deadline': update_deadline,
        'Tags': update_tags,
        'Back': move_back,
    }

    while True:
        console.clear()
        print_task_summary(task)

        action = prompt_menu(update_handlers.keys())
        handler = update_handlers[action]

        try:
            console.clear()
            handler(task)

        except BackToMenuError:
            save_todo_list()
            return
        except UpdateCancelledError:
            continue

        console.print('\n[green]Updated successfully.[/green]')
        typer.pause()
