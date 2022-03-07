import shutil
from pathlib import Path

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
        root_sass_file="inputs/theme.scss",
        root_qss_file="outputs/theme.qss",
    )
