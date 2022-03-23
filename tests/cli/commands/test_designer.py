"""Tests for qt_dev_helper.cli.commands.designer"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable
from typing import Sequence

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests.conftest import CallQtToolKwargs
from typer.testing import CliRunner

import qt_dev_helper.cli.commands.designer as designer_cli_module
from qt_dev_helper.cli.main_app import app


@pytest.mark.parametrize(
    "cli_options, expected_max_path_slice_index",
    (
        ((), 4),
        (("--no-recurse-folder",), 2),
        (("--no-open-files",), 1),
        (("--no-recurse-folder", "--no-open-files"), 1),
    ),
)
def test_designer(
    monkeypatch: MonkeyPatch,
    nested_ui_folder: tuple[Path, Path, Path, Path],
    mock_call_qt_tool: tuple[Callable[..., None], CallQtToolKwargs],
    cli_options: Sequence[str],
    expected_max_path_slice_index: int,
):
    """designer CLI calls call_qt_tool with correct args."""
    runner = CliRunner()
    mock_func, call_kwargs = mock_call_qt_tool
    tmp_path = nested_ui_folder[0]
    with monkeypatch.context() as m:
        m.setattr(designer_cli_module, "call_qt_tool", mock_func)
        m.setattr(os, "curdir", tmp_path.as_posix())
        result = runner.invoke(app, ["designer", *cli_options])

        assert result.exit_code == 0, result.stdout

        assert call_kwargs["tool_name"] == "designer"
        assert call_kwargs["no_wait"] is True

        assert len(call_kwargs["arguments"]) == expected_max_path_slice_index - 1
        for expected_path in nested_ui_folder[1:expected_max_path_slice_index]:
            assert expected_path.as_posix() in call_kwargs["arguments"]
