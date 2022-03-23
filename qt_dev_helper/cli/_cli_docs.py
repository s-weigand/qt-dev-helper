"""Module used to to autogenerate CLI documentation with sphinx_click."""
import typer

from qt_dev_helper.cli.main_app import app

typer_click_object = typer.main.get_command(app)
