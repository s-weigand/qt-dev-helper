"""Module containing functionality to transpile resources *.scss, *.ui and *.qrc."""
from __future__ import annotations

from pathlib import Path
from typing import Callable
from typing import Literal
from typing import Sequence
from typing import cast

import qtsass
import rich

from qt_dev_helper.config import Config
from qt_dev_helper.config import QtDevHelperConfigError
from qt_dev_helper.config import RccKwargs
from qt_dev_helper.config import UicKwargs
from qt_dev_helper.config import load_config
from qt_dev_helper.qt_tools import call_qt_tool
from qt_dev_helper.utils import find_matching_files
from qt_dev_helper.utils import format_rel_output_path


def transpile_sass(sass_file: str | Path, qss_file: str | Path) -> Path:
    """Transpile scss file to qss.

    This function differs from ``qtsass.compile_filename`` in that
    it ensures that the output file is utf8 encoded.

    Parameters
    ----------
    sass_file: str | Path
        Path to the sass input file.
    qss_file: str | Path
        Path to output the compiled qss file to.

    Returns
    -------
    Path
        Absolute path to the compiled qss file.
    """
    sass_file = Path(sass_file).resolve()
    qss = qtsass.compile(
        sass_file.read_text(encoding="utf8"),
        include_paths=[sass_file.parent.as_posix()],
    )
    qss_file = Path(qss_file).resolve()
    qss_file.parent.mkdir(parents=True, exist_ok=True)
    qss_file.write_text(cast(str, qss), encoding="utf8")
    return qss_file


def compile_ui_file(
    ui_file: str | Path,
    output_path: str | Path,
    *,
    generator: Literal["python", "cpp"] = "python",
    form_import: bool = True,
    uic_args: Sequence[str] = (),
) -> Path:
    """Call 'Qt User Interface Compiler' to create code from a ui file.

    Parameters
    ----------
    ui_file: str | Path
        Path to the ui file.
    output_path: str | Path
        Path the output file should be saved to.
    generator: Literal["python", "cpp"]
        Language to generate code for. Defaults to "python"
    form_import: bool
        Sets the '--from-imports' flag when used with python. Defaults to True
    uic_args: Sequence[str]
        Additional args for 'uic' (use '--help' for details). Defaults to ()

    Returns
    -------
    Path
        Path of the compiled file
    """
    options = ["-g", generator]
    if generator == "python" and form_import is True:
        options.append("--from-imports")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args = (Path(ui_file).as_posix(), "-o", output_path.as_posix(), *options, *uic_args)

    call_qt_tool("uic", arguments=args)
    return output_path


def compile_resource_file(
    qrc_file: str | Path,
    output_path: str | Path,
    *,
    generator: Literal["python", "cpp"] = "python",
    rcc_args: Sequence[str] = (),
) -> Path:
    """Call 'Qt Resource Compiler' to create code from a resource file.

    Parameters
    ----------
    qrc_file: str | Path
        Path to the resource file.
    output_path: str | Path
        Path the output file should be saved to.
    generator: Literal["python", "cpp"]
        Language to generate code for. Defaults to "python"
    rcc_args: Sequence[str]
        Additional args for 'rcc' (use '--help' for details). Defaults to ()

    Returns
    -------
    Path
        Path of the compiled file
    """
    options = ["-g", generator]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args = (Path(qrc_file).as_posix(), "-o", output_path.as_posix(), *options, *rcc_args)

    call_qt_tool("rcc", arguments=args)
    return output_path


def build_uis(
    ui_files_folder: Path,
    generated_ui_code_folder: Path,
    *,
    flatten_path: bool = True,
    uic_kwargs: UicKwargs | None = None,
    log_function: Callable[..., None] = rich.print,
    recurse_folder: bool = True,
) -> list[Path]:
    """Compile ui files by iterating over all ui files in a folder.

    Parameters
    ----------
    ui_files_folder: Path
        Base path containing the input ui files.
    generated_ui_code_folder: Path
        Base path to save generated code from ui files to.
    flatten_path: bool
        Whether or not to flatten the folder structure of the ui files
        (For the 'python'generator this should be True in order for imports
        to resolve). Defaults to True
    uic_kwargs: UicKwargs | None
        Keyword arguments passed to the uic executable. Defaults to None
    log_function: Callable[..., None]
        Function used to print log messages. Defaults to rich.print
    recurse_folder: bool
        Whether or not to recurse directories searching for files. Defaults to True

    Returns
    -------
    list[Path]
        List of generated files.

    See Also
    --------
    compile_ui_file
    """
    built_files = []
    if uic_kwargs is None:
        uic_kwargs = {}
    for ui_file in find_matching_files([ui_files_folder], "*.ui", recurse_folder=recurse_folder):
        rel_out_path = format_rel_output_path(
            ui_files_folder,
            Path(ui_file),
            "Ui_{file_stem}.py",
            flatten_path=flatten_path,
        )
        if uic_kwargs.get("generator", "python") == "cpp":
            rel_out_path = rel_out_path.with_suffix(".h")
        out_file = generated_ui_code_folder / rel_out_path
        log_function(f"Creating: {rel_out_path.as_posix()}")
        built_file = compile_ui_file(ui_file, out_file, **uic_kwargs)
        built_files.append(built_file)
    return built_files


def build_resources(
    resource_folder: Path,
    generated_rc_code_folder: Path,
    *,
    flatten_path: bool = True,
    rcc_kwargs: RccKwargs | None = None,
    log_function: Callable[..., None] = rich.print,
    recurse_folder: bool = True,
) -> list[Path]:
    """Compile qrc files by iterating over all qrc files in a folder.

    Parameters
    ----------
    resource_folder: Path
        Base path containing the input qrc files.
    generated_rc_code_folder: Path
        Base path to save generated code from qrc files to.
    flatten_path: bool
        Whether or not to flatten the folder structure of the ui files
        (For the 'python'generator this should be True in order for imports
        to resolve). Defaults to True
    rcc_kwargs: RccKwargs | None
        Keyword arguments passed to the rcc executable. Defaults to None
    log_function: Callable[..., None]
        Function used to print log messages. Defaults to rich.print
    recurse_folder: bool
        Whether or not to recurse directories searching for files. Defaults to True

    Returns
    -------
    list[Path]
        List of generated files.
    """
    built_files = []
    if rcc_kwargs is None:
        rcc_kwargs = {}
    for resource_file in find_matching_files(
        [resource_folder], "*.qrc", recurse_folder=recurse_folder
    ):
        rel_out_path = format_rel_output_path(
            resource_folder,
            Path(resource_file),
            "{file_stem}_rc.py",
            flatten_path=flatten_path,
        )
        if rcc_kwargs.get("generator", "python") == "cpp":
            rel_out_path = rel_out_path.with_suffix(".h")
        out_file = generated_rc_code_folder / rel_out_path
        log_function(f"Creating: {rel_out_path.as_posix()}")
        built_file = compile_resource_file(resource_file, out_file, **rcc_kwargs)
        built_files.append(built_file)
    return built_files


def build_all_assets(
    config: Config | str | Path,
    log_function: Callable[..., None] = rich.print,
    recurse_folder: bool = True,
) -> list[Path]:
    """Build all assets based on the provided configuration.

    This can be used in the built script when using source distributions.

    Parameters
    ----------
    config: Config
        Configuration to use for building assets.
        If a path is passed it will try to find the config.
    log_function: Callable[..., None]
        Function used to print log messages. Defaults to rich.print
    recurse_folder: bool
        Whether or not to recurse directories searching for files. Defaults to True

    Returns
    -------
    list[Path]
        List of generated files.

    See Also
    --------
    .load_config
    """
    if not isinstance(config, Config):
        config = load_config(config)
    built_files = []
    try:
        sass_file, qss_file = config.root_style_paths()
        log_function(f"Creating: {qss_file.relative_to(config.base_path).as_posix()}")
        built_files += [transpile_sass(sass_file, qss_file)]
    except QtDevHelperConfigError:
        log_function("No style files to compile fund in config!")
    try:
        built_files += build_uis(
            *config.ui_folder_paths(),
            flatten_path=config.flatten_folder_structure,
            uic_kwargs=config.uic_kwargs(),
            log_function=log_function,
            recurse_folder=recurse_folder,
        )
    except QtDevHelperConfigError:
        log_function("No ui folders fund in config!")
    try:
        built_files += build_resources(
            *config.rc_folder_paths(),
            flatten_path=config.flatten_folder_structure,
            rcc_kwargs=config.rcc_kwargs(),
            log_function=log_function,
            recurse_folder=recurse_folder,
        )
    except QtDevHelperConfigError:
        log_function("No resource folders fund in config!")

    return built_files
