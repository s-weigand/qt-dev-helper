"""Tests for ``qt_dev_helper.qt_tools``."""
from __future__ import annotations

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from qt_dev_helper.qt_tools import QtToolExecutionError
from qt_dev_helper.qt_tools import QtToolNotFoundError
from qt_dev_helper.qt_tools import call_qt_tool
from qt_dev_helper.qt_tools import find_qt_tool


def test_find_qt_tool():
    """When PySide6 is installed use pyside6-rcc"""
    assert "pyside6-rcc" in find_qt_tool("rcc")


def test_find_qt_tool_not_found(monkeypatch: MonkeyPatch):
    """Raise error if qt tool can't be found."""
    with monkeypatch.context() as m:
        m.setenv("path", "")
        with pytest.raises(QtToolNotFoundError) as exc_info:
            find_qt_tool.__wrapped__("rcc")

        assert str(exc_info.value) == (
            "Can not find Qt tool tool_name='rcc' please install a Qt distributions. "
            "E.g. 'pip install PySide6'."
        )


def test_call_qt_tool(capfd: CaptureFixture):
    """Basic test calling help on uic."""
    call_qt_tool("uic", arguments=("--help",))

    assert "Qt User Interface Compiler version" in capfd.readouterr().out


def test_call_qt_tool_exception():
    """Raise Except if arguments is of wrong type or bad options are passed."""
    with pytest.raises(ValueError) as exc_info:
        call_qt_tool("uic", arguments=("--help"))

    assert str(exc_info.value) == (
        "arguments needs to be of type Sequence[str],\n Got:\n\targuments='--help'"
    )

    with pytest.raises(QtToolExecutionError) as exc_info:
        call_qt_tool("uic", arguments=("--invalid-option",))

    assert "Unknown option 'invalid-option'." in str(exc_info.value)
