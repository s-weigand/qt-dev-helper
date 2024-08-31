"""Module containing the CLI designer command implementations."""

from __future__ import annotations

import os
from pathlib import Path

from typer import Argument
from typer import Option

from qt_dev_helper.qt_tools import call_qt_tool
from qt_dev_helper.utils import find_matching_files


def designer(  # noqa: DOC
    files: list[Path] = Argument(
        default=None,
        exists=True,
        help="File/Folder which should be opened by the designer. "
        "If not provided the current directory will be used.",
    ),
    recurse_folder: bool = Option(
        default=True,
        is_flag=True,
        help="Whether or not to recurse directories searching for files.",
    ),
    open_files: bool = Option(
        default=True,
        is_flag=True,
        help="Whether or not to open files.",
    ),
) -> None:
    """Open *.ui files in qt-designer."""
    files = files or [Path(os.curdir)]

    if open_files is False:
        args: tuple[str, ...] = ()
    else:
        args = find_matching_files(files, "*.ui", recurse_folder=recurse_folder)
    call_qt_tool("designer", arguments=args, no_wait=True)
