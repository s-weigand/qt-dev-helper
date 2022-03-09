from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError
from tests import TEST_DATA

from qt_dev_helper.config import Config
from qt_dev_helper.config import QtDevHelperConfigError
from qt_dev_helper.config import RccKwargs
from qt_dev_helper.config import UicKwargs
from qt_dev_helper.config import load_toml_config


@pytest.mark.parametrize(
    "root_sass_file, root_qss_file",
    (("assets/styles/theme.scss", None), (None, "output/theme.qss")),
)
def test_config_validate_style_paths_asymmetric(
    root_sass_file: str | None, root_qss_file: str | None
):
    """Raise error is only one style is defined."""
    with pytest.raises(ValidationError) as exc_info:
        Config(base_path=TEST_DATA, root_sass_file=root_sass_file, root_qss_file=root_qss_file)
    assert "The values of 'root_sass_file' and 'root_qss_file' need either be both" in str(
        exc_info.value
    )


@pytest.mark.parametrize(
    "ui_files_folder, generated_ui_code_folder",
    (("assets/ui_files", None), (None, "outputs/ui_files")),
)
def test_config_validate_ui_paths_asymmetric(
    ui_files_folder: str | None, generated_ui_code_folder: str | None
):
    """Raise error is only one path is defined."""
    with pytest.raises(ValidationError) as exc_info:
        Config(
            base_path=TEST_DATA,
            ui_files_folder=ui_files_folder,
            generated_ui_code_folder=generated_ui_code_folder,
        )
    assert (
        "The values of 'ui_files_folder' and 'generated_ui_code_folder' need either be both"
        in str(exc_info.value)
    )


@pytest.mark.parametrize(
    "resource_folder, generated_rc_code_folder",
    (("assets", None), (None, "outputs/rc")),
)
def test_config_validate_rc_paths_asymmetric(
    resource_folder: str | None, generated_rc_code_folder: str | None
):
    """Raise error is only one path is defined."""
    with pytest.raises(ValidationError) as exc_info:
        Config(
            base_path=TEST_DATA,
            resource_folder=resource_folder,
            generated_rc_code_folder=generated_rc_code_folder,
        )
    assert (
        "The values of 'resource_folder' and 'generated_rc_code_folder' need either be both"
        in str(exc_info.value)
    )


@pytest.mark.parametrize(
    "var_name, var_value",
    (
        ("root_sass_file", "not_a_path"),
        ("root_sass_file", "assets/styles"),
        ("ui_files_folder", "not_a_path"),
        ("ui_files_folder", "assets/styles/theme.scss"),
        ("resource_folder", "not_a_path"),
        ("resource_folder", "assets/styles/theme.scss"),
    ),
)
def test_config_validate_path_exists_or_none(var_name: str, var_value: str):
    with pytest.raises(ValidationError) as exc_info:
        Config(base_path=TEST_DATA, **{var_name: var_value})
    assert f"The value of {var_name!r} needs to be a valid path or None." in str(exc_info.value)


def test_config_path_extraction(dummy_config: Config):
    """Extract resolved paths from config"""

    base_path = dummy_config.base_path

    root_sass_file, root_qss_file = dummy_config.root_style_paths()

    assert root_sass_file == base_path / "assets/styles/theme.scss"
    assert root_qss_file == base_path / "outputs/theme.qss"

    ui_files_folder, generated_ui_code_folder = dummy_config.ui_folder_paths()

    assert ui_files_folder == base_path / "assets/ui_files"
    assert generated_ui_code_folder == base_path / "outputs/ui_files"

    resource_folder, generated_rc_code_folder = dummy_config.rc_folder_paths()

    assert resource_folder == base_path / "assets"
    assert generated_rc_code_folder == base_path / "outputs/ui_files"


def test_config_path_extraction_exception(dummy_config: Config):
    """Raise error if any path is None."""
    dummy_config.root_qss_file = None

    with pytest.raises(QtDevHelperConfigError) as exc_info:
        dummy_config.root_style_paths()

    assert str(exc_info.value).startswith(
        "Both 'root_sass_file' and 'root_qss_file' need to be defined.\n"
    )


def test_config_uic_kwargs(dummy_config: Config):
    """Kwargs for uic are same as in config."""

    expected: UicKwargs = {"generator": "python", "form_import": True, "uic_args": ["--idbased"]}

    assert dummy_config.uic_kwargs() == expected


def test_config_rcc_kwargs(dummy_config: Config):
    """Kwargs for rcc are same as in config."""

    expected: RccKwargs = {"generator": "python", "rcc_args": ["--compress-algo", "zlib"]}

    assert dummy_config.rcc_kwargs() == expected


def test_load_toml_config(dummy_config: Config):
    """Load config from test toml config."""

    assert load_toml_config(dummy_config.base_path / "pyproject.toml") == dummy_config


def test_load_toml_config_no_tool_config(tmp_path: Path):
    """Load config without config for qt-dev-helper."""
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text("[tool.black]\nline-length = 99")

    assert load_toml_config(config_file) == Config(base_path=config_file.parent)
