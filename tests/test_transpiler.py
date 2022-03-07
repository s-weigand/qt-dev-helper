from __future__ import annotations

import re
from pathlib import Path

from tests import EXPECTED_TEST_DATA
from tests import INPUT_TEST_DATA

from qt_dev_helper.config import Config
from qt_dev_helper.transpiler import compile_resource_file
from qt_dev_helper.transpiler import compile_ui_file
from qt_dev_helper.transpiler import transpile_sass


def test_transpile_sass(tmp_path: Path, dummy_config: Config):
    """Transpiling scss gives the expected result."""

    expected = (EXPECTED_TEST_DATA / "theme.qss").read_text()

    out_file = transpile_sass(INPUT_TEST_DATA / "theme.scss", tmp_path / "theme.qss")

    assert out_file.read_text(encoding="utf8") == expected

    out_file = transpile_sass(*dummy_config.root_style_paths())

    assert out_file.read_text(encoding="utf8") == expected


def test_tranpile_ui_file(dummy_config: Config):
    """Create python or cpp header from ui file."""
    tmp_path = dummy_config.base_path

    ui_file = tmp_path / "inputs/minimal_ui.ui"
    result = compile_ui_file(ui_file, tmp_path / "default.py")

    assert result.read_text() == (EXPECTED_TEST_DATA / "minimal_ui.py").read_text()

    result = compile_ui_file(ui_file, tmp_path / "default_no_from.py", form_import=False)

    assert result.read_text() == (EXPECTED_TEST_DATA / "minimal_ui_no_from_imports.py").read_text()

    result = compile_ui_file(ui_file, tmp_path / "minimal_ui.h", generator="cpp")

    assert result.read_text() == (EXPECTED_TEST_DATA / "minimal_ui.h").read_text()


def test_tranpile_resource_file(dummy_config: Config):
    """Create python or cpp header from ui file."""
    tmp_path = dummy_config.base_path
    qrc_file = tmp_path / "inputs/test_resource.qrc"
    result = compile_resource_file(qrc_file, tmp_path / "resource.py")

    assert result.read_text() == (EXPECTED_TEST_DATA / "test_resource.py").read_text()

    result = compile_resource_file(qrc_file, tmp_path / "resource.h", generator="cpp")

    # comment_blank_line_pattern
    cbl_pattern = re.compile(r"(\n\s*|\s*[/]{2}.+?)\n")

    assert re.sub(cbl_pattern, "\n", result.read_text()) == re.sub(
        cbl_pattern, "\n", (EXPECTED_TEST_DATA / "test_resource.h").read_text()
    )
