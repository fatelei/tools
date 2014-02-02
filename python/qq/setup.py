#!/usr/bin/python
#-*-coding: utf8-*-

from setuptools import find_packages, setup


install_requires = ['requests',
                     'lxml']

entry_points = """
    [console_scripts]
    qq=qqtools.app:run
"""

setup(
    name="qq",
    author="fatelei@gmail.com",
    version="0.1",
    install_requires=install_requires,
    entry_points=entry_points,
    package_dir={"": "apps"},
    packages=find_packages("apps")
)
