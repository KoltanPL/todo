from typing import TYPE_CHECKING

from src.cli.commands.add_task import add_task
from src.cli.commands.flow_update import update_task
from src.cli.commands.interactive import interactive
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task


if TYPE_CHECKING:
    from typer import Typer  # pragma: no cover


def register_commands(app: Typer) -> None:
    """
    Register all CLI commands in the Typer application.

    This function binds command handlers to the provided Typer instance,
    making them available as CLI commands.

    Args:
        app (Typer): The Typer application instance.
    """
    app.command()(list_tasks)
    app.command()(add_task)
    app.command()(remove_task)
    app.command()(interactive)
    app.command()(update_task)
