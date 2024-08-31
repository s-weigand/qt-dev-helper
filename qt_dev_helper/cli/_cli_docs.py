"""Module used to to autogenerate CLI documentation with sphinx_click."""

from __future__ import annotations

import typer

from qt_dev_helper.cli.main_app import app

typer_click_object = typer.main.get_command(app)
