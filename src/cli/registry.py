from typer import Typer

from src.cli.commands.interactive import interactive
from src.cli.commands.add_task import add_task
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task


def register_commands(app: Typer) -> None:
    app.command()(list_tasks)
    app.command()(add_task)
    app.command()(remove_task)
    app.command()(interactive)
