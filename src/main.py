import typer

from src.cli.commands import register_commands


app = typer.Typer(name='todo-app', help='A professional Todo CLI application')

register_commands(app)


if __name__ == '__main__':
    app()
