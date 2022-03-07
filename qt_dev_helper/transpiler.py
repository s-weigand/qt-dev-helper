"""Module containing functionality to transpile resources *.sass, *.ui and *.qrc."""
from __future__ import annotations

from pathlib import Path
from typing import cast

import qtsass


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
