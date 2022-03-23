from setuptools import setup

from qt_dev_helper.transpiler import build_all_assets

build_all_assets(__file__)


setup()
