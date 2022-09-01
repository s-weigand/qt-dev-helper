"""Tests for the `qt_dev_helper``` cli main command."""

import re
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner

from qt_dev_helper.cli.main_app import app


def test_missing_cli_extra_requires(monkeypatch: MonkeyPatch):
    """Exception raised if cli extra_requires is missing"""
    with monkeypatch.context() as m:
        m.delitem(sys.modules, "qt_dev_helper.cli.main_app")
        m.setitem(sys.modules, "typer", None)

        with pytest.raises(ImportError, match=r"pip install qt-dev-helper\[cli\]"):
            import qt_dev_helper.cli.main_app  # noqa: F401


def test_main():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Collection of CLI commands" in result.output
    help_result = runner.invoke(app, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(
        r"--help.*?Show this message and exit\.", help_result.output
    ), help_result.output
