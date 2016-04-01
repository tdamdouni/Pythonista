from __future__ import absolute_import
import os

from .parser import parse
from .todos import Todos
from .compatibility import read, write, unicode


def from_text(text):
    """Load todos from text"""
    return parse(text)


def from_path(path):
    """
    Load todos from file

    Note:
        Saves source so todos can be later saved using `to_sources`
    """
    text = read(path)
    todos = parse(text)
    todos.set_source(path)
    return todos


def from_paths(paths):
    """Load all todos stored in `paths` and join them in signle todos."""
    todos = Todos()
    for path in paths:
        subtodos = from_path(path)
        project_title = _get_project_title(path)
        subtodos = subtodos.as_subtodos_of(project_title)
        todos += subtodos
    return todos


def _get_project_title(path):
    filename = os.path.split(path)[1]
    return os.path.splitext(filename)[0] + ':'


def from_dir(path, extension='.taskpaper'):
    """Load all todos in directory and join them in single todos."""
    return from_paths(
        _list_files_in_dir(path, extension)
    )


def _list_files_in_dir(path, extension='.taskpaper'):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(extension):
                yield os.path.join(root, filename)


def to_path(todos, path):
    """Save todos to given path."""
    write(path, unicode(todos))


def to_sources(todos):
    """Save todos to files that they were read from."""
    for subtodos in todos.iter_sourced():
        to_path(subtodos, subtodos.get_source())
