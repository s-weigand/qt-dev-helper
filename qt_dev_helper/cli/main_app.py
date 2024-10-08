"""Main CLI application definition."""

from __future__ import annotations

try:
    import typer
except ImportError as error:
    msg = (
        "The requirements for the cli usage are not installed.\n"
        "Install qt-dev-helper with the cli extras e.g.:\n`pip install qt-dev-helper[cli]`"
    )
    raise ImportError(msg) from error

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
