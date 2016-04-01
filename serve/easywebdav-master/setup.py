import os
import functools
from setuptools import setup, find_packages

_IN_PACKAGE_DIR = functools.partial(os.path.join, "easywebdav")

with open(_IN_PACKAGE_DIR("__version__.py")) as version_file:
    exec(version_file.read())

properties = dict(
    name="easywebdav",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.3",
        ],
    description="A straight-forward WebDAV client, implemented using Requests",
    license="ISC",
    author="Amnon Grossman",
    author_email="emesh1@gmail.com",
    url="http://github.com/amnong/easywebdav",
    version=__version__,  # noqa
    packages=find_packages(exclude=["tests"]),
    data_files = [],
    install_requires=[
        "requests",
        ],
    entry_points=dict(
        console_scripts=[],
        ),
    )

# Properties for development environments
if "EASYWEBDAV_DEV" in os.environ:
    properties["install_requires"].append((
        "nose",
        "yanc",
        "PyWebDAV",
        ))

setup(**properties)