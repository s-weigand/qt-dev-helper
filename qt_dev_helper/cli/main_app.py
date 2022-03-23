"""Main CLI application definition."""

import typer

from qt_dev_helper.cli.commands.build import build
from qt_dev_helper.cli.commands.designer import designer

app = typer.Typer(
    name="qt-dev-helper",
    no_args_is_help=True,
    help="Collection of CLI commands to improve workflows when developing Qt GUI Applications.",
)

app.command()(designer)
app.command()(build)


if __name__ == "__main__":
    app()
