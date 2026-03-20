from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

import questionary
from questionary import Style
import typer

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.ui.console import console


if TYPE_CHECKING:
    from collections.abc import Iterable  # pragma: no cover

style = Style([
    ('highlighted', 'fg:#ffffff bg:#44475a bold'),
    ('pointer', 'fg:#50fa7b bold'),
    ('selected', 'fg:#50fa7b'),
    ('question', 'bold'),
])


def prompt_description() -> str:
    """Prompt the user for a task description.

    Repeats the prompt until a valid description (at least 3 characters)
    is provided.

    Returns:
        str: Validated task description.
    """
    while True:
        description = typer.prompt('Task description').strip()
        if len(description) > 2:
            return description
        console.print('[red]Description must be at least 3 characters.[/red]')


def prompt_priority() -> PriorityEnum:
    """Prompt the user to select a task priority.

    Displays a graphical selection menu with available priorities.

    Returns:
        PriorityEnum: Selected priority.

    Raises:
        typer.Abort: If the user cancels the selection.
    """
    options = [p.name.title() for p in PriorityEnum]

    answer = questionary.select('Choose priority: ', choices=options, style=style).ask()

    if answer is None:
        raise typer.Abort()

    return PriorityEnum[answer.upper()]


def prompt_status() -> StatusEnum:
    """Prompt the user to select a task status.

    Displays a graphical selection menu with available statuses.

    Returns:
        StatusEnum: Selected status.

    Raises:
        typer.Abort: If the user cancels the selection.
    """
    options = [s.value.title().replace('_', ' ') for s in StatusEnum]
    answer = questionary.select('Choose status: ', choices=options, style=style).ask()

    if answer is None:
        raise typer.Abort()

    return StatusEnum(answer.lower().replace(' ', '_'))


def prompt_deadline_graphical() -> date | None:
    """Prompt the user to select or input a task deadline.

    Provides predefined options (today, tomorrow, etc.) or allows the user
    to enter a custom date in ISO format (YYYY-MM-DD). Custom dates must
    be in the future.

    Returns:
        date | None: Selected deadline or None if no deadline is chosen.

    Raises:
        typer.Abort: If the user cancels the selection.
    """

    options = [
        'No deadline',
        'Today',
        'Tomorrow',
        'In 7 days',
        'In 14 days',
        'Pick exact date (YYYY-MM-DD)',
    ]

    answer = questionary.select('Choose deadline: ', choices=options, style=style).ask()
    if answer is None:
        raise typer.Abort()

    today = datetime.now(UTC).date()

    if answer == 'No deadline':
        return None
    if answer == 'Today':
        return today
    if answer == 'Tomorrow':
        return today + timedelta(days=1)
    if answer == 'In 7 days':
        return today + timedelta(days=7)
    if answer == 'In 14 days':
        return today + timedelta(days=14)

    while True:
        raw = typer.prompt('Deadline (YYYY-MM-DD)').strip()

        try:
            parsed = date.fromisoformat(raw)
        except ValueError:
            typer.echo('Invalid format. Example: 2026-03-01')
        else:
            if parsed <= today:
                typer.echo('Date must be in the future.')
                continue

            return parsed


def prompt_tags() -> list[str]:
    """Prompt the user for task tags.

    Accepts a comma-separated string and returns a cleaned list of tags.

    Returns:
        list[str]: List of trimmed, non-empty tags.
    """
    raw = typer.prompt('Task tags (comma separated)', default='').strip()

    if not raw:
        return []

    return [tag.strip() for tag in raw.split(',') if tag.strip()]


def prompt_menu(choices: Iterable[str]) -> str:
    """Prompt the user to select an option from a menu.

    Args:
        choices (Iterable[str]): Available menu options.

    Returns:
        str: Selected option.

    Raises:
        typer.Abort: If the user cancels the selection.
    """
    return questionary.select('Menu', choices=list(choices), style=style).ask()
