
from setuptools import setup

setup(
    app=['photoDistributor_MAC.py'],
    data_files=[('assets', ['assets/background.jpg'])],
    setup_requires=['py2app'],
)