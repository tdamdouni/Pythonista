# TodoFlow 4.0

![](icon.png)

TodoFlow is Python module that provides functions to parse, filter, search, modify and save todo lists stored in plain text files with TaskPaper syntax.

## Changelog

- 2015-10-02 - 4.0.2 
    - Removal of ply pickle file so TodoFlow can work with ply 3.6 with no errors
    - Release on PyPI
- 2015-04-24 - Removal of workflows
- 2014-10-24 - Release of version 4
    - **this version removes some features and introduces breaking changes** 
    - new code base
    - queries are now parsed with [ply](https://github.com/dabeaz/ply)
    - for now removes support for [Editorial.app](http://omz-software.com/editorial/)
    - workflows start from zero
    - new icons
    - setup.py
    - python3 compatiblity

## Installation

    pip install TodoFlow

## Overview

### Loading todos

Load and parse todos using one of this functions:

- `todos = todoflow.from_text(text)`
- `todos = todoflow.from_path(path)`
- `todos = todoflow.from_paths(paths)` - todos from several files are joined into one
- `todos = todoflow.from_dir(path, extension='.taskpaper')` - every todo file in given direcotry is joined into one todos

```
    todos = todoflow.from_text("""
    project 1:
        - task 1
        - task 2 @today
    """)
```

### Saving todos

- `todoflow.to_path(todos, path)` - save todos to file
- `todoflow.to_sources(todos)` - when todos are loaded from file (using `from_path`, `from_paths` or `from_dir`) they store path to source file so they can be saved to it later

#### Todos

Todos - collection of todo items.
Todos are immutable.

- `todos.filter(query)` - returns new Todos, with only those that match query or their parents, analogous to searching in Taskpaper.app
- `todos.search(query)` - returns iterator of Todoitems that match query (and only them).

```
    print(todos.filter('not @today'))

    >>> project 1:
    >>>     - task 1

    print(tuple(todos.search('task')))

    >>> (<Todoitem: 2 | "task 1" | task>, <Todoitem: 3 | "task 2 @done" | task>)
```

#### Queries

Subset with few additions of query syntax of Taskpaper.app is supported:

- searching by text
- searching by @tag
- searching by tag parameter: @tag *op* text
- searching by project: project *op* text
- searching by type: `type = task`, `type = note`, `type = "project"`
- including subitems: `+d`
- narrowing to only first items that match query: `+f`
- *op*s: `=`, `<=`, `<`, `>`, `>=`, `!=`, `->` (in), `<-` (contains)
- logical operators: `and`, `or`, `not`
- parentheses: `(`, `)`...

### Todo item

Todo items are mutable, their changes are visible in all todos that contain them.

- `tag(tag_to_use, param=None)`
- `remove_tag(tag_to_remove)`
- `has_tag(tag)`
- `get_tag_param(tag)`
- `edit(new_text)`
- `change_to_task()`
- `change_to_project()`
- `change_to_note()`
- `change_to_empty_line()`

```
    for item in todos.search('@today'):
        item.tag('@done', '2014-10-24')
        item.remove_tag('@today')
    print(todos)

    >>> project 1:
    >>>    - task 1
    >>>    - task 2 @done(2014-10-24)
```

## textutils

Module `todoflow.textutils` provides functions
that operate on text and are used internally in todoflow but can be
useful outside of it:

- `is_task(text)`
- `is_project(text)`
- `is_note(text)`
- `has_tag(text, tag)`
- `get_tag_param(text, tag)`
- `remove_tag(text, tag)`
- `replace_tag(text, tag, replacement)`
- `add_tag(text, tag, param=None)`
- `enclose_tag(text, tag, prefix, suffix=None)`
- `get_all_tags(text, include_indicator=False)`
- `modify_tag_param(text, tag, modification)`
- `sort_by_tag_param(texts_collection, tag, reverse=False)`
