"""Module containing the CLI build command implementations."""
import os
from pathlib import Path
from typing import Optional

from typer import Argument
from typer import Option

from qt_dev_helper.cli.utils import parse_optional_args_string
from qt_dev_helper.config import CodeGenerators
from qt_dev_helper.config import Config
from qt_dev_helper.config import ConfigNotFoundError
from qt_dev_helper.config import load_config
from qt_dev_helper.transpiler import build_all_assets


def build(
    base_path: Optional[Path] = Argument(
        default=None,
        help="Base path used to resolve relative paths, by default the path to a found config.",
    ),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        file_okay=True,
        help="Path to a config file.",
    ),
    recurse_folder: bool = Option(
        False,
        "--recurse-folder",
        "-r",
        is_flag=True,
        help="Recurse directories searching for files.",
    ),
    generator: Optional[CodeGenerators] = Option(
        None,
        "--generator",
        "-g",
        help="Code generator used to compile ui and resource files.",
    ),
    flatten_folder_structure: Optional[bool] = Option(
        default=None,
        is_flag=True,
        help="Whether or not to flatten the folder structure of the ui and resource files.",
    ),
    ui: bool = Option(
        default=True,
        is_flag=True,
        help="Whether or not to build ui files from '*.ui' files.",
    ),
    ui_files_folder: Optional[Path] = Option(
        default=None,
        dir_okay=True,
        help="Root folder containing *.ui files.",
    ),
    generated_ui_code_folder: Optional[Path] = Option(
        default=None,
        help="Root folder to save code generated from *.ui files to.",
    ),
    uic_args: Optional[str] = Option(
        default=None,
        help="Additional arguments for the uic executable, as comma separated list.",
    ),
    rc: bool = Option(
        default=True,
        is_flag=True,
        help="Whether or not to build resource files from '*.qrc' files.",
    ),
    resource_folder: Optional[Path] = Option(
        default=None,
        dir_okay=True,
        help="Root folder containing *.qrc files.",
    ),
    generated_rc_code_folder: Optional[Path] = Option(
        default=None,
        help="Root folder to save code generated from *.qrc files to.",
    ),
    form_import: Optional[bool] = Option(
        default=None,
        help="Python: generate imports relative to '.'",
    ),
    rcc_args: Optional[str] = Option(
        default=None,
        help="Additional arguments for the rcc executable, as comma separated list.",
    ),
    qss: bool = Option(
        default=True,
        is_flag=True,
        help="Whether or not to build qss files from '*.scss' files.",
    ),
    root_sass_file: Optional[Path] = Option(
        default=None,
        file_okay=True,
        help="Scss stylesheet with the style for the whole application.",
    ),
    root_qss_file: Optional[Path] = Option(
        default=None,
        help=(
            "Qss stylesheet with the style for the whole application, "
            "generated from 'root_sass_file'."
        ),
    ),
) -> None:
    """Build production assets from input files."""
    try:
        config_obj = load_config(config)
    except ConfigNotFoundError:
        config_obj = Config(base_path=base_path or Path(os.curdir))

    if base_path is not None:
        config_obj.base_path = base_path

    config_obj.update(
        {
            "generator": generator,
            "flatten_folder_structure": flatten_folder_structure,
            "ui_files_folder": ui_files_folder,
            "generated_ui_code_folder": generated_ui_code_folder,
            "uic_args": parse_optional_args_string(uic_args),
            "form_import": form_import,
            "resource_folder": resource_folder,
            "generated_rc_code_folder": generated_rc_code_folder,
            "rcc_args": parse_optional_args_string(rcc_args),
            "root_sass_file": root_sass_file,
            "root_qss_file": root_qss_file,
        }
    )

    if qss is False:
        config_obj.deactivate_style_build()
    if ui is False:
        config_obj.deactivate_ui_build()
    if rc is False:
        config_obj.deactivate_resource_build()

    build_all_assets(config=config_obj, recurse_folder=recurse_folder)
