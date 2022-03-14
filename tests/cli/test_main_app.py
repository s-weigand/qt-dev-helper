#!/usr/bin/env python

"""Tests for `qt_dev_helper` package."""

import re

import pytest
from typer.testing import CliRunner

# from qt_dev_helper import qt_dev_helper
from qt_dev_helper.cli.main_app import app


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "qt_dev_helper.cli.main" in result.output
    help_result = runner.invoke(app, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help\s+Show this message and exit.", help_result.output)
