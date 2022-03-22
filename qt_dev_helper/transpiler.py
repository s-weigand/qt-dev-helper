"""Module containing functionality to transpile resources *.sass, *.ui and *.qrc."""
from __future__ import annotations

from pathlib import Path
from typing import Literal
from typing import Sequence
from typing import cast

import qtsass

from qt_dev_helper.qt_tools import call_qt_tool


def transpile_sass(
    sass_file: str | Path,
    qss_file: str | Path,
) -> Path:
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
    if generator == "python" and form_import:
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
