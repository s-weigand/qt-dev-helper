"""Tests for qt_dev_helper.cli.commands.designer"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner

import qt_dev_helper.cli.commands.build as build_cli_module
from qt_dev_helper.cli.main_app import app
from qt_dev_helper.config import Config


def test_build(monkeypatch: MonkeyPatch, dummy_config: Config):
    """Autodiscover config."""
    runner = CliRunner()
    call_kwargs = {}

    def mock_func(**kwargs):
        call_kwargs.update(kwargs)

    with monkeypatch.context() as m:
        m.setattr(build_cli_module, "build_all_assets", mock_func)
        m.setattr(os, "curdir", (dummy_config.base_path / "assets").as_posix())
        result = runner.invoke(app, ["build"])

        assert result.exit_code == 0, result.stdout

        assert call_kwargs["config"].dict() == dummy_config.dict()


@pytest.mark.parametrize(
    "flag, none_attr_names",
    (
        ("--no-ui", ("ui_files_folder", "generated_ui_code_folder")),
        ("--no-rc", ("resource_folder", "generated_rc_code_folder")),
        ("--no-qss", ("root_sass_file", "root_qss_file")),
    ),
)
def test_build_cli_deactivate(
    monkeypatch: MonkeyPatch, dummy_config: Config, flag: str, none_attr_names: tuple[str, str]
):
    """Deactivate build parts."""
    runner = CliRunner()
    call_kwargs = {}

    def mock_func(**kwargs):
        call_kwargs.update(kwargs)

    with monkeypatch.context() as m:
        m.setattr(build_cli_module, "build_all_assets", mock_func)
        m.setattr(os, "curdir", (dummy_config.base_path / "assets").as_posix())
        result = runner.invoke(app, ["build", flag])

        assert result.exit_code == 0, result.stdout

        result_cfg = call_kwargs["config"].dict()
        expected_cfg = dummy_config.dict()

        for none_attr_name in none_attr_names:
            assert result_cfg[none_attr_name] is None

            del result_cfg[none_attr_name]
            del expected_cfg[none_attr_name]

        assert result_cfg == expected_cfg


@pytest.mark.parametrize("pass_base_path", (True, False))
def test_build_cli_no_config(monkeypatch: MonkeyPatch, tmp_path: Path, pass_base_path: bool):
    """Deactivate build parts."""
    runner = CliRunner()
    call_kwargs = {}

    def mock_func(**kwargs):
        call_kwargs.update(kwargs)

    with monkeypatch.context() as m:
        m.setattr(build_cli_module, "build_all_assets", mock_func)
        m.setattr(os, "curdir", tmp_path.as_posix())
        expected_base_path = tmp_path

        cmds = ["build"]

        if pass_base_path:
            expected_base_path = tmp_path / "foo/bar"
            expected_base_path.mkdir(parents=True, exist_ok=True)
            cmds.append(expected_base_path.as_posix())

        result = runner.invoke(app, cmds)

        assert result.exit_code == 0, result.stdout

        assert call_kwargs["config"].base_path.samefile(expected_base_path)
