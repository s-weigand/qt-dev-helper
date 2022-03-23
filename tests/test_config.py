from __future__ import annotations

import os
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pydantic import ValidationError
from tests import REPO_ROOT
from tests import TEST_DATA

from qt_dev_helper.config import Config
from qt_dev_helper.config import ConfigNotFoundError
from qt_dev_helper.config import QtDevHelperConfigError
from qt_dev_helper.config import RccKwargs
from qt_dev_helper.config import UicKwargs
from qt_dev_helper.config import find_config
from qt_dev_helper.config import load_config
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


def test_config_deactivate_style_build(dummy_config: Config):
    """Style related paths are ``None``."""
    dummy_config.deactivate_style_build()

    assert dummy_config.root_sass_file is None
    assert dummy_config.root_qss_file is None


def test_config_deactivate_ui_build(dummy_config: Config):
    """Ui related paths are ``None``."""
    dummy_config.deactivate_ui_build()

    assert dummy_config.ui_files_folder is None
    assert dummy_config.generated_ui_code_folder is None


def test_config_deactivate_resource_build(dummy_config: Config):
    """Resource related paths are ``None``."""
    dummy_config.deactivate_resource_build()

    assert dummy_config.resource_folder is None
    assert dummy_config.generated_rc_code_folder is None


def test_config_update(dummy_config: Config):
    """Update values if not None."""
    dummy_config.update(
        {"generator": "cpp", "flatten_folder_structure": False, "root_sass_file": None},
    )

    assert dummy_config.generator.value == "cpp"
    assert dummy_config.flatten_folder_structure is False
    assert dummy_config.root_sass_file == "assets/styles/theme.scss"


def test_config_update_errors(dummy_config: Config):
    """."""
    with pytest.raises(ValidationError) as exec_info:
        dummy_config.update({"root_sass_file": None}, filter_none=False)

    assert "The values of 'root_sass_file' and 'root_qss_file' need either be both" in str(
        exec_info.value
    )

    with pytest.raises(ValidationError) as exec_info:
        dummy_config.update({"invalid_name": "foo"})

    assert "extra fields not permitted" in str(exec_info.value)


def test_load_toml_config(dummy_config: Config):
    """Load config from test toml config."""

    assert (
        load_toml_config(dummy_config.base_path / "pyproject.toml").dict() == dummy_config.dict()
    )


def test_load_toml_config_no_tool_config(tmp_path: Path):
    """Load config without config for qt-dev-helper."""
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text("[tool.black]\nline-length = 99")

    with pytest.raises(ConfigNotFoundError) as exec_info:
        load_toml_config(config_file)

    assert str(exec_info.value).startswith("Could not find 'qt-dev-helper' config in ")


@pytest.mark.parametrize(
    "start_path, config_file_name, expected",
    (
        (REPO_ROOT, "pyproject.toml", REPO_ROOT / "pyproject.toml"),
        (REPO_ROOT, "setup.cfg", REPO_ROOT / "setup.cfg"),
        (TEST_DATA, "pyproject.toml", TEST_DATA / "pyproject.toml"),
        (TEST_DATA.parent, "pyproject.toml", REPO_ROOT / "pyproject.toml"),
        (None, "pyproject.toml", REPO_ROOT / "pyproject.toml"),
    ),
)
def test_find_config(
    monkeypatch: MonkeyPatch, start_path: Path, config_file_name: str, expected: Path
):
    """Find config file using different start paths or file names."""
    with monkeypatch.context() as m:
        m.setattr(os, "curdir", Path(__file__).parent.as_posix())
        result = find_config(start_path, config_file_name)

        assert result.samefile(expected)


def test_find_config_error(tmp_path: Path):
    """Raise error if file can not be found."""
    with pytest.raises(ConfigNotFoundError) as exec_info:
        find_config(tmp_path)

    assert str(exec_info.value) == "Could not find config file 'pyproject.toml'."


@pytest.mark.parametrize("rel_path", ("", "assets/styles/theme.scss"))
def test_load_config(dummy_config: Config, rel_path: str):
    """Load config also works when path is a file which isn't the config file."""

    result = load_config(dummy_config.base_path / rel_path)

    assert result.dict() == dummy_config.dict()


def test_load_config_error(dummy_config: Config):
    """On error parsing config."""
    config_file = dummy_config.base_path / "pyproject.toml"
    config_file.write_text("[tool.black]\nline-length = 99")

    with pytest.raises(ConfigNotFoundError) as exec_info:
        load_config(dummy_config.base_path)

    assert (
        str(exec_info.value) == "No config file containing 'qt-dev-helper' config could be found."
    )
