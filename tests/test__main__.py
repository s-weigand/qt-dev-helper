"""Test calling qt-dev-helper as module."""
import re
import subprocess
import sys


def test_module_invocation():
    """Just check that the CLI gets invoked."""
    result = subprocess.run([sys.executable, "-m", "qt_dev_helper", "--help"], capture_output=True)

    assert result.returncode == 0
    assert re.search(
        r"--help.*?Show this message and exit\.", result.stdout.decode()
    ), result.stdout.decode()
