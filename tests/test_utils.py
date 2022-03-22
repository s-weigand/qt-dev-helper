"""Tests for qt_dev_helper.utils ."""

from __future__ import annotations

from pathlib import Path

import pytest

from qt_dev_helper.utils import find_matching_files
from qt_dev_helper.utils import format_rel_output_path


@pytest.mark.parametrize(
    "format_string, flatten_path, expected",
    (
        ("Ui_{file_stem}.py", True, "Ui_dummy.py"),
        ("{file_stem}_rc.py", True, "dummy_rc.py"),
        ("Ui_{file_stem}.py", False, "widgets/Ui_dummy.py"),
    ),
)
def test_format_rel_output_path(format_string: str, flatten_path: bool, expected: str):
    """Rel out paths are formatted correct."""
    root_folder = Path("assets/ui_files")
    file_path = Path("assets/ui_files/widgets/dummy.ui")

    result = format_rel_output_path(
        root_folder, file_path, format_string, flatten_path=flatten_path
    )

    assert result == Path(expected)


@pytest.mark.parametrize(
    "recurse_folder, max_index",
    (
        (True, 4),
        (False, 2),
    ),
)
def test_find_matching_files(
    nested_ui_folder: tuple[Path, Path, Path, Path], recurse_folder: bool, max_index: int
):
    """Find nested ui files."""
    tmp_path = nested_ui_folder[0]
    result = find_matching_files([tmp_path], "*.ui", recurse_folder=recurse_folder)

    assert len(result) == max_index - 1

    for expected in nested_ui_folder[1:max_index]:
        assert expected.as_posix() in result


@pytest.mark.parametrize(
    "recurse_folder",
    (
        (True),
        (False),
    ),
)
def test_find_matching_files_single_file(
    nested_ui_folder: tuple[Path, Path, Path, Path], recurse_folder: bool
):
    """Single file."""
    tmp_path = nested_ui_folder[1]
    result = find_matching_files([tmp_path], "*.ui", recurse_folder=recurse_folder)

    assert result == (nested_ui_folder[1].as_posix(),)


def test_find_matching_files_not_matching(tmp_path: Path):
    """File doesn't match pattern."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    result = find_matching_files([test_file], "*.ui")

    assert result == ()
