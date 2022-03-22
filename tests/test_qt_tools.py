"""Tests for ``qt_dev_helper.qt_tools``."""
from __future__ import annotations

import os
import sys

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from qt_dev_helper.qt_tools import QtToolExecutionError
from qt_dev_helper.qt_tools import QtToolNotFoundError
from qt_dev_helper.qt_tools import call_qt_tool
from qt_dev_helper.qt_tools import extend_qt_tool_path
from qt_dev_helper.qt_tools import find_qt_tool


@pytest.mark.parametrize("package_name", ("pyside6", "qt5_applications", "qt6_applications"))
def test_extend_qt_tool_path(package_name: str):
    """All supported tools are on the extended path"""
    assert package_name in extend_qt_tool_path().lower()


def test_extend_qt_tool_path_missing_module(monkeypatch: MonkeyPatch):
    """Return path if none of the modules is installed."""
    with monkeypatch.context() as m:
        from qt_dev_helper import qt_tools

        def mock_package_path(*args):
            raise ModuleNotFoundError()

        m.setattr(qt_tools, "package_path", mock_package_path)

        assert extend_qt_tool_path.__wrapped__() == os.environ.get("path", "")


def test_find_qt_tool():
    """When PySide6 is installed use rcc from the PySide6 package."""
    assert (
        "site-packages/pyside6/rcc" in find_qt_tool("rcc").lower()
        or "site-packages/pyside6/qt/libexec/rcc" in find_qt_tool("rcc").lower()
    )


def test_find_qt_tool_not_found(monkeypatch: MonkeyPatch):
    """Raise error if qt tool can't be found."""
    with monkeypatch.context() as m:
        from qt_dev_helper import qt_tools

        m.setattr(qt_tools, "extend_qt_tool_path", lambda: "")
        with pytest.raises(QtToolNotFoundError) as exc_info:
            find_qt_tool.__wrapped__("rcc")

        assert str(exc_info.value) == (
            "Can not find Qt tool tool_name='rcc' please install a Qt distributions. "
            "E.g. 'pip install PySide6'."
        )


@pytest.mark.skipif(
    "CI" in os.environ and sys.platform == "win32",
    reason="On the windows github runner this opens a dialog which can't be closed.",
)
def test_call_qt_tool(capfd: CaptureFixture):
    """Basic test calling help on uic."""
    call_qt_tool("uic", arguments=("--help",))

    assert "Qt User Interface Compiler version" in capfd.readouterr().out


def test_call_qt_tool_no_wait(capfd: CaptureFixture):
    """Do not wait for process to finish."""
    call_qt_tool("uic", arguments=("--help",), no_wait=True)

    assert capfd.readouterr().out == ""


@pytest.mark.skipif(
    "CI" in os.environ and sys.platform == "win32",
    reason="On the windows github runner this opens a dialog which can't be closed.",
)
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
