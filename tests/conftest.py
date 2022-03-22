from __future__ import annotations

import shutil
from pathlib import Path
from typing import Sequence
from typing import TypedDict

import pytest
from tests import TEST_DATA

from qt_dev_helper.config import Config


@pytest.fixture
def dummy_config(tmp_path: Path):
    """Copy test data to temp folder and create config."""
    shutil.copytree(
        TEST_DATA,
        tmp_path,
        ignore=shutil.ignore_patterns("expected"),
        dirs_exist_ok=True,
    )

    yield Config(
        base_path=tmp_path,
        root_sass_file="assets/styles/theme.scss",
        root_qss_file="outputs/theme.qss",
        generator="python",
        flatten_folder_structure=True,
        ui_files_folder="assets/ui_files",
        generated_ui_code_folder="outputs/ui_files",
        uic_args=["--idbased"],
        form_import=True,
        resource_folder="assets",
        generated_rc_code_folder="outputs/ui_files",
        rcc_args=["--compress-algo", "zlib"],
    )


@pytest.fixture
def nested_ui_folder(tmp_path: Path):
    """Nested folder structure with *.ui files."""
    nested_folder = tmp_path / "foo/bar"
    nested_folder.mkdir(parents=True, exist_ok=True)
    file1 = tmp_path / "foo.ui"
    file1.write_text("foo")
    (tmp_path / "test.txt").write_text("test")
    file2 = tmp_path / "foo/bar.ui"
    file2.write_text("bar")
    file3 = tmp_path / "foo/bar/baz.ui"
    file3.write_text("baz")
    yield (tmp_path, file1, file2, file3)


class CallQtToolKwargs(TypedDict, total=False):
    """Typing helper class."""

    tool_name: str
    arguments: Sequence[str]
    no_wait: bool


@pytest.fixture
def mock_call_qt_tool():
    call_kwargs: CallQtToolKwargs = {}

    def mock_func(tool_name: str, *, arguments: Sequence[str] = (), no_wait: bool = False):
        call_kwargs["tool_name"] = tool_name
        call_kwargs["arguments"] = arguments
        call_kwargs["no_wait"] = no_wait

    yield mock_func, call_kwargs
