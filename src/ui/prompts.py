from datetime import date, timedelta

import questionary
import typer

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


def prompt_priority() -> PriorityEnum:
    options = [p.name.title() for p in PriorityEnum]

    answer = questionary.select('Choose priority: ', choices=options).ask()

    if answer is None:
        raise typer.Abort()

    return PriorityEnum[answer.upper()]


def prompt_status() -> StatusEnum:
    """
    Prompt user to choose task status.
    """
    options = [s.value for s in StatusEnum]
    answer = questionary.select('Choose status: ', choices=options).ask()

    if answer is None:
        raise typer.Abort()

    return StatusEnum(answer)


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

    answer = questionary.select('Choose deadline: ', choices=options).ask()
    if answer is None:
        raise typer.Abort()

    today = date.today()

    if answer == 0:
        return None
    if answer == 1:
        return today
    if answer == 2:
        return today + timedelta(days=1)
    if answer == 3:
        return today + timedelta(days=7)
    if answer == 4:
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
