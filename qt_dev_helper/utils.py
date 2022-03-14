"""Module containing utility functionality."""

from __future__ import annotations

from pathlib import Path


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
