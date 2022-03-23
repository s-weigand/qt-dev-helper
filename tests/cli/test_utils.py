"""Tests for qt_dev_helper.cli.utils"""

from __future__ import annotations

import pytest

from qt_dev_helper.cli.utils import parse_optional_args_string


@pytest.mark.parametrize(
    "optional_args_string, expected",
    (
        (None, None),
        ("", []),
        ("  ", []),
        ("--opt, arg  ", ["--opt", "arg"]),
    ),
)
def test_parse_optional_args_string(optional_args_string: str | None, expected: list[str] | None):
    """Args are split and striped"""
    assert parse_optional_args_string(optional_args_string) == expected
