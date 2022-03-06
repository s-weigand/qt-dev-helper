"""Console script for qt_dev_helper."""
import typer

app = typer.Typer()


@app.command()
def main(args=None) -> int:
    """Console script for qt_dev_helper.

    Parameters
    ----------
    args : list, optional
        Commandlineargs, by default None

    Returns
    -------
    int
        Returncode
    """
    typer.echo("Replace this message by putting your code into " "qt_dev_helper.cli.main")
    typer.echo("See click documentation at https://typer.tiangolo.com/")
    return 0


if __name__ == "__main__":
    app()
