# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/s-weigand/qt-dev-helper/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Qt Dev Helper could always use more documentation, whether as part of the
official Qt Dev Helper docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/s-weigand/qt-dev-helper/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `qt_dev_helper` for local development.

1. Fork the `qt-dev-helper` repo on GitHub.

2. Clone your fork locally:

   ```bash
   $ git clone git@github.com:your_name_here/qt_dev_helper.git
   ```

3. Install your local copy into a virtualenv. Assuming you have hatch installed (`pipx install hatch`),
   this is how you set up your fork for local development:

   ```bash
   $ cd qt-dev-helper/
   $ hatch shell
   ```

4. Install the `pre-commit` hooks (to install `pre-commit` run `pipx install pre-commit`):

   ```bash
   $ pre-commit install
   ```

5. Create a branch for local development:

   ```bash
   $ git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the tests:

   ```bash
   $ pytest
   ```

   To get flake8 and tox, just pip install them into your virtualenv.

7. Commit your changes and push your branch to GitHub:

   ```bash
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```

8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 3.9, 3.10, 3.11 and 3.12. Check
   https://github.com/s-weigand/qt-dev-helper/actions
   and make sure that the tests pass for all supported Python versions.

> [!TIP]
> To run a subset of tests:

> ```bash
> $ pytest tests.test_qt_dev_helper
> ```
