"""Tests for qt_dev_helper.cli.commands.designer"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

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
    "flag, replace_attrs",
    (
        ("--no-ui", {"ui_files_folder": None, "generated_ui_code_folder": None}),
        ("--no-rc", {"resource_folder": None, "generated_rc_code_folder": None}),
        ("--no-qss", {"root_sass_file": None, "root_qss_file": None}),
        ("--no-use-prefix-paths", {"prefix_paths": []}),
    ),
)
def test_build_cli_deactivate(
    monkeypatch: MonkeyPatch, dummy_config: Config, flag: str, replace_attrs: dict[str, Any]
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

        for key, value in replace_attrs.items():
            if value is None:
                assert result_cfg[key] is value
            else:
                assert result_cfg[key] == value

            del result_cfg[key]
            del expected_cfg[key]

        assert result_cfg == expected_cfg, result.stdout


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
