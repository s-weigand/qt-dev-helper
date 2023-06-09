"""Main CLI application definition."""

try:
    import typer
except ImportError as error:
    raise ImportError(
        "The requirements for the cli usage are not installed.\n"
        "Install qt-dev-helper with the cli extras e.g.:\n"
        "`pip install qt-dev-helper[cli]`"
    ) from error

from qt_dev_helper.cli.commands.build import build
from qt_dev_helper.cli.commands.designer import designer

app = typer.Typer(
    name="qt-dev-helper",
    no_args_is_help=True,
    help="Collection of CLI commands to improve workflows when developing Qt GUI Applications.",
)

app.command()(designer)
app.command()(build)

try:
    from trogon import Trogon
    from typer.main import get_group

    def tui(ctx: typer.Context) -> None:
        """Terminal User Interface to build and run CLI command."""
        Trogon(get_group(app), click_context=ctx).run()

except ImportError:

    def tui(ctx: typer.Context) -> None:
        """Not available install 'Trogon' or 'qt-dev-helper[tui]'."""
        print(
            "Install 'Trogon' or qt-dev-helper with the TUI extras e.g.:",
            "`pip install qt-dev-helper[tui]` or install ",
        )


app.command()(tui)

if __name__ == "__main__":
    app()
