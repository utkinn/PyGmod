#!/usr/bin/env python3
# pylint: disable=missing-docstring

from setuptools import setup, Extension

setup(
    name='PyGmod',
    packages=['gmod', 'pygmod'],
    ext_modules=[Extension('pygmod._luastack', sources=['../cpp/_luastack.cpp'],
                           include_dirs=['../cpp/'])],
    setup_requires=['pytest-runner'],
    tests_require=[
        'coverage',
        'pytest',
        'pytest-cov',
        'pytest-pylint'
    ],
    zip_safe=False
)
