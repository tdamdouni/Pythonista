#!/usr/bin/env python
from distutils.core import setup


setup(
    name="python-readability",
    author="Tim Cuthbertson",
    author_email="tim3d.junk+github@gmail.com",
    description="python port of arc90's readability bookmarklet",
    long_description=open("README").read(),
    license="Apache License 2.0",
    url="http://github.com/gfxmonk/python-readability",
    packages=[
        "readability",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
