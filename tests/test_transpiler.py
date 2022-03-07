from __future__ import annotations

from pathlib import Path

from tests import EXPECTED_TEST_DATA
from tests import INPUT_TEST_DATA

from qt_dev_helper.config import Config
from qt_dev_helper.transpiler import transpile_sass


def test_transpile_sass(tmp_path: Path, dummy_config: Config):
    """Transpiling scss gives the expected result."""

    expected = (EXPECTED_TEST_DATA / "theme.qss").read_text()

    out_file = transpile_sass(INPUT_TEST_DATA / "theme.scss", tmp_path / "theme.qss")

    assert out_file.read_text(encoding="utf8") == expected

    out_file = transpile_sass(*dummy_config.root_style_paths())

    assert out_file.read_text(encoding="utf8") == expected
