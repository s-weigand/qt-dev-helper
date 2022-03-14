from pathlib import Path

import pytest

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
