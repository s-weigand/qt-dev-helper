"""Qt implementation cross compatibility module."""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
from collections.abc import Sequence
from functools import lru_cache
from importlib.resources import path as package_path
from pathlib import Path


class QtToolNotFoundError(Exception):
    """Error thrown when a Qt tool can't be found.

    See Also
    --------
    find_qt_tool
    """

    def __init__(self, tool_name: str) -> None:
        super().__init__(
            f"Can not find Qt tool {tool_name=} please install a Qt distributions. "
            "E.g. 'pip install PySide6'."
        )


class QtToolExecutionError(Exception):
    """Error thrown when a Qt tool returns a non-zero exit status code.

    See Also
    --------
    call_qt_tool
    """

    def __init__(self, returncode: int, cmd: str, stdout: bytes, stderr: bytes) -> None:
        output = (stdout + b"\n\n" + stderr).decode()
        super().__init__(
            f"Command {cmd!r} returned non-zero exit status {returncode}.\n"
            f"Command output:\n{output}"
        )


@lru_cache(maxsize=1)
def extend_qt_tool_path() -> str:
    """Prepend path variable with package dirs to qt-tools if present.

    Returns
    -------
    str
        Path extended with library executable paths.
    """
    additional_paths: list[str] = []
    # package_name: rel_path_to_include
    tool_packages = {
        "PySide6": ["", "Qt/libexec"],
        "qt6_applications": ["Qt/bin"],
        "qt5_applications": ["Qt/bin"],
    }
    for package, rel_paths in tool_packages.items():
        with contextlib.suppress(ModuleNotFoundError):
            with package_path(package, "__init__.py") as p:
                additional_paths += [str(p.parent / rel_path) for rel_path in rel_paths]
    return os.pathsep.join((*additional_paths, os.environ.get("path", "")))


@lru_cache
def find_qt_tool(tool_name: str) -> str:
    """Find path to Qt tool executable like ``rcc``, ``uic`` or ``designer``.

    Parameters
    ----------
    tool_name: str
        Name of the Qt tool to look up.

    Returns
    -------
    str
        Path to the tool executable.

    Raises
    ------
    QtToolNotFoundError
        If the tool could not be found in the path.
    """
    extended_path = extend_qt_tool_path()
    command_path = shutil.which(tool_name, path=extended_path)
    if command_path is not None:
        return Path(command_path).as_posix()
    raise QtToolNotFoundError(tool_name)


def call_qt_tool(tool_name: str, *, arguments: Sequence[str] = (), no_wait: bool = False) -> None:
    """Call qt tools in a generic way.

    Parameters
    ----------
    tool_name: str
        Name of the Qt tool to use (e.g. ``rcc``, ``uic`` or ``designer``)
    arguments: Sequence[str]
        Additional arguments for options for the tool. Defaults to ()
    no_wait: bool
        Whether or not to wait for the process to finish
        (used for CLI not to wait for designer application to close). Defaults to False

    Raises
    ------
    ValueError
        If ``arguments`` is not of type Sequence[str]
    QtToolExecutionError
        If the tool returns a non-zero exit code.
    """
    if not isinstance(arguments, Sequence) or isinstance(arguments, str):
        raise ValueError(f"arguments needs to be of type Sequence[str],\n Got:\n\t{arguments=}")
    tool_exe = find_qt_tool(tool_name)

    cmd = " ".join((tool_exe, *arguments))

    if no_wait is True:
        subprocess.Popen(
            cmd,
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=True,
        )
    else:
        out = subprocess.run(cmd, capture_output=True, shell=True)

        if out.returncode != 0:
            raise QtToolExecutionError(
                returncode=out.returncode, cmd=cmd, stdout=out.stdout, stderr=out.stderr
            )

        print(out.stdout.decode())
