"""Module containing utility functionality."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
from typing import Sequence


def format_rel_output_path(
    root_folder: Path, file_path: Path, format_string: str, *, flatten_path: bool = True
) -> Path:
    """Format ``file_path`` to a relative path for output files.

    Parameters
    ----------
    root_folder: Path
        Root folder of the file resides in.
    file_path: Path
        Path to the file to be formatted.
    format_string: str
        String with format instruction 'file_stem' (e.g. 'Ui_{file_stem}.py').
    flatten_path: bool
        Whether or not to persist the original folder structure. Defaults to True

    Returns
    -------
    Path
        Relative path in respect to ``root_folder`` for the formatted file.
    """
    rel_file_parent_path = Path("")
    file_name = format_string.format(file_stem=file_path.stem)
    if flatten_path is False:
        rel_file_parent_path = file_path.relative_to(root_folder).parent

    return rel_file_parent_path / file_name


def find_matching_files(
    files: Sequence[Path], file_pattern: str, *, recurse_folder: bool = True
) -> tuple[str, ...]:
    """Search for files matching ``file_pattern``.

    Parameters
    ----------
    files: Sequence[Path]
        List of paths (files or folders) to check for matching files.
    file_pattern: str
        Pattern to match files, this a Unix shell-style pattern and nto an regex.
    recurse_folder: bool
        Whether or not to recurse directories searching for files. Defaults to True

    Returns
    -------
    tuple[str,...]
        Tuple of posix conform string paths to files matching ``file_pattern``.
    """
    file_paths = set()
    for path in files:
        if path.is_dir() is True:
            glob_func = path.rglob if recurse_folder is True else path.glob

            for file in glob_func(file_pattern):
                file_paths.add(file.as_posix())
        if path.is_file() and fnmatch(path.as_posix(), file_pattern) is not False:
            file_paths.add(path.as_posix())
    return tuple(file_paths)
