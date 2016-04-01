#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='TodoFlow',
    version='4.0.2',
    description='taskpaper in python',
    author='Piotr Wilczyński',
    author_email='wilczynski.pi@gmail.com',
    url='https://github.com/bevesce/TodoFlow',
    packages=['todoflow'],
    install_requires=[
        "ply",
    ],
)
