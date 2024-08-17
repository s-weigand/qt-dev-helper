# Qt Dev Helper

[![PyPi Version](https://img.shields.io/pypi/v/qt_dev_helper.svg)](https://pypi.org/project/qt-dev-helper/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/qt_dev_helper.svg)](https://pypi.org/project/qt-dev-helper/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/qt-dev-helper.svg)](https://anaconda.org/conda-forge/qt-dev-helper)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Actions Status](https://github.com/s-weigand/qt-dev-helper/workflows/Tests/badge.svg)](https://github.com/s-weigand/qt-dev-helper/actions)
[![Documentation Status](https://readthedocs.org/projects/qt-dev-helper/badge/?version=latest)](https://qt-dev-helper.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/s-weigand/qt-dev-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/s-weigand/qt-dev-helper)
[![Documentation Coverage](https://raw.githubusercontent.com/s-weigand/qt-dev-helper/main/docs/_static/interrogate_badge.svg)](https://github.com/s-weigand/qt-dev-helper)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![All Contributors](https://img.shields.io/github/all-contributors/s-weigand/qt-dev-helper)](#contributors)

Toolbox to help develop Qt applications, improving the usability of the existing tooling.

## Installation

```console
pip install qt-dev-helper
```

OR

```console
conda install -c conda-forge qt-dev-helper
```

## Features

- Usable as Library and/or CLI tool
- Compatible with [PEP517](https://peps.python.org/pep-0517/) build system
  ([see test case](https://github.com/s-weigand/qt-dev-helper/blob/main/tests/data/pyproject.toml))
- CLI auto completion
- Project wide configuration in `pyproject.toml`
- Recursive asset compiler for Qt projects (using `uic` and `rcc`):
  - `*.ui` -> `*.py`
  - `*.qrc` -> `*.py`
  - `*.ui` -> `*.h`
  - `*.qrc` -> `*.h`
  - `*.scss` -> `*.qss`
- Support for multiple Qt tooling suppliers
  - `PySide6-Essentials`
  - `qt6-applications`
  - `qt5-applications`
- Ability to open all files in a folder in QtDesigner

## Planned features

- Stand alone executable for each release (Windows)
- File watch mode
- `qss` injection into `*.ui` files
- [`pre-commit`](https://pre-commit.com/) hooks

## FAQ

- Q: Why is `PyQt5` not supported?

  A: `PyQt5` only ships a python specific version of `uic` and `rcc` breaking the tool API and
  compatibility with cpp projects.
  Use the matching version of `qt5-applications` as Qt tooling supplier.

## Contributors ✨

Thanks goes out to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/s-weigand"><img src="https://avatars.githubusercontent.com/u/9513634?v=4?s=100" width="100px;" alt="Sebastian Weigand"/><br /><sub><b>Sebastian Weigand</b></sub></a><br /><a href="https://github.com/s-weigand/qt-dev-helper/commits?author=s-weigand" title="Code">💻</a> <a href="#ideas-s-weigand" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-s-weigand" title="Maintenance">🚧</a> <a href="#projectManagement-s-weigand" title="Project Management">📆</a> <a href="#infra-s-weigand" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/s-weigand/qt-dev-helper/commits?author=s-weigand" title="Tests">⚠️</a> <a href="https://github.com/s-weigand/qt-dev-helper/commits?author=s-weigand" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jsnel"><img src="https://avatars.githubusercontent.com/u/3616369?v=4?s=100" width="100px;" alt="Joris Snellenburg"/><br /><sub><b>Joris Snellenburg</b></sub></a><br /><a href="https://github.com/s-weigand/qt-dev-helper/pulls?q=is%3Apr+reviewed-by%3Ajsnel" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-jsnel" title="Maintenance">🚧</a> <a href="#infra-jsnel" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!
