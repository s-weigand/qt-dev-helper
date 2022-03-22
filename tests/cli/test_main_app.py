#!/usr/bin/env python

"""Tests for `qt_dev_helper` package."""

import re

from typer.testing import CliRunner

from qt_dev_helper.cli.main_app import app


def test_main():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Collection of CLI commands" in result.output
    help_result = runner.invoke(app, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help\s+Show this message and exit.", help_result.output)
