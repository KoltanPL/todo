from datetime import date, timedelta

import typer
from simple_term_menu import TerminalMenu

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


def prompt_priority() -> PriorityEnum:
    options = [p.name.title() for p in PriorityEnum]
    menu = TerminalMenu(options)

    idx = menu.show()
    if idx is None:
        raise typer.Abort()

    return PriorityEnum[options[idx].upper()]


def prompt_status() -> StatusEnum:
    """
    Prompt user to choose task status.
    """
    options = [s.value for s in StatusEnum]
    menu = TerminalMenu(options)

    idx = menu.show()
    if idx is None:
        raise typer.Abort()

    return StatusEnum(options[idx])


def prompt_deadline_graphical() -> date | None:
    """
    Prompt user for deadline using graphical menu.
    """

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

    today = date.today()

    if idx == 0:
        return None
    if idx == 1:
        return today
    if idx == 2:
        return today + timedelta(days=1)
    if idx == 3:
        return today + timedelta(days=7)
    if idx == 4:
        return today + timedelta(days=14)

    while True:
        raw = typer.prompt('Deadline (YYYY-MM-DD)').strip()

        try:
            parsed = date.fromisoformat(raw)

            if parsed <= today:
                typer.echo('Date must be in the future.')
                continue

            return parsed

        except ValueError:
            typer.echo('Invalid format. Example: 2026-03-01')


def prompt_tags() -> list[str]:
    """
    Prompt user for comma-separated tags.
    """
    raw = typer.prompt('Task tags (comma separated)', default='').strip()

    if not raw:
        return []

    return [tag.strip() for tag in raw.split(',') if tag.strip()]
