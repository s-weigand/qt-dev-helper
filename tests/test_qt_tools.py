from __future__ import annotations

"""Tests for ``qt_dev_helper.qt_tools``."""
import pytest
from _pytest.monkeypatch import MonkeyPatch

from qt_dev_helper.qt_tools import QtToolNotFoundError
from qt_dev_helper.qt_tools import find_qt_tool


def test_find_qt_tool():
    pass


def test_find_qt_tool_not_found(monkeypatch: MonkeyPatch):
    """Raise error if qt tool can't be found."""
    with monkeypatch.context() as m:
        m.setenv("path", "")
        with pytest.raises(QtToolNotFoundError) as exc_info:
            find_qt_tool("rcc")

        assert str(exc_info.value) == (
            "Can not find Qt tool tool_name='rcc' please install a Qt distributions. "
            "E.g. 'pip install PySide6'."
        )
