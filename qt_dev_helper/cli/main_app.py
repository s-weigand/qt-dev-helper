"""Main CLI application definition."""
from typing import List
from typing import Union

import typer

from qt_dev_helper.cli.commands.designer import designer

app = typer.Typer(
    name="qt-dev-helper",
    no_args_is_help=True,
    help="Collection of CLI commands to improve workflows when developing Qt GUI Applications.",
)

app.command()(designer)


@app.command()
def main(args: Union[List[str], None] = None) -> int:
    """Console script for qt_dev_helper."""
    typer.echo("Replace this message by putting your code into " "qt_dev_helper.cli.main")
    typer.echo("See click documentation at https://typer.tiangolo.com/")
    return 0


if __name__ == "__main__":
    app()
