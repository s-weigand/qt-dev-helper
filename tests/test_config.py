import pytest
from pydantic import ValidationError
from tests import TEST_DATA

from qt_dev_helper.config import Config
from qt_dev_helper.config import load_toml_config


@pytest.mark.parametrize(
    "root_sass_file, root_qss_file", (("input/theme.scss", None), (None, "output/theme.qss"))
)
def test_config_validate_styles(root_sass_file: str, root_qss_file: str):
    """Raise error is only one style is defined."""
    with pytest.raises(ValidationError):
        Config(base_path=TEST_DATA, root_sass_file=root_sass_file, root_qss_file=root_qss_file)


def test_load_toml_config(dummy_config: Config):
    """Load config from test toml config."""

    assert load_toml_config(dummy_config.base_path / "pyproject.toml") == dummy_config
