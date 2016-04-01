# -*- coding: utf-8 -*-
from collections import deque

from .todoitem import Todoitem
from .querying_parser import parse as parse_query
from .printers import PlainPrinter
from .compatibility import _str_


class Todos(object):
    """Representation of taskpaper todos."""
    def __init__(self, todos_tree=None, source=None):
        self._todos_tree = todos_tree or Node()
        self._source = source
        self._todos_tree.source = source

    def __iter__(self):
        return self._todos_tree.iter_values()

    def __unicode__(self):
        return PlainPrinter().unicode(self._todos_tree) if self._todos_tree else u''

    def __str__(self):
        return _str_(self)

    def __len__(self):
        return len(self._todos_tree)

    def __add__(self, other):
        return Todos(self._todos_tree + other._todos_tree)

    def __div__(self, query):
        """Filter todos by query"""
        # I know it's inresponsible but is't so cool
        return self.filter(query)

    def set_source(self, path):
        self._source = path
        self._todos_tree.source = path

    def get_source(self):
        if self._source:
            return self._source
        else:
            return self._todos_tree.source

    def search(self, query):
        """
        Args:
            query (text)

        Returns:
            Iterator of `Todoitem`s that match query.
        """
        return self._todos_tree.search(parse_query(query))

    def filter(self, query):
        """
        Args:
            query (text)

        Returns:
            New `Todos` with only items that match query and their parents.
            Analogous to filter from Taskpaper.app.

        Example:
            Filtering todos::
                project 1:
                    - task 1
                        - subtask 1
                    - task 2
                project 2:
                    - task 3
            with query 'subtask 1' gives::
                project 1:
                    - task 1
                        - subtask 1
        """
        filtered_tree = self._todos_tree.filter(
            parse_query(query)
        )
        return Todos(filtered_tree, source=self._source)

    def get_item(self, query):
        """
        Args:
            query (text)

        Returns:
            Firest `Todoitem` that matches query.
        """
        for i in self.search(query):
            return i

    def as_subtodos_of(self, text):
        if self._todos_tree.get_value():
            children = [self._todos_tree]
        else:
            children = self._todos_tree.get_children()
        return Todos(
            Node(
                value=Todoitem(text),
                children=children
            ),
            source=self._source
        )

    def by_appending(self, text, to_item):
        item = Todoitem(text)
        return Todos(
            self._todos_tree.append_child_to_node_with_value(item, value=to_item),
            source=self.get_source()
        )

    def by_prepending(self, text, to_item):
        item = Todoitem(text)
        return Todos(
            self._todos_tree.prepend_child_to_node_with_value(item, value=to_item),
            source=self.get_source()
        )

    def iter_sourced(self):
        """
        Yield new Todos that contain only items that were read from some file
        and their subitems.
        """
        for node in self._todos_tree:
            if node.source:
                yield Todos(
                    Node(children=node.get_children()),
                    source=node.source
                )


class Node(object):
    """Internal representation of todos.

    Todos are represented as ordered Forest. `Node` holds this structure.

    - `Node` can be a Forest when _value is None, then _children are set of Trees.
    - `Node` also can a single Tree, then it holds `Todoitem` in _value and Tree of subitems in _children.

    Attributes:
        _value (object): item stored in node
        _parent (Node, optional): None when this is the root `Node`
        _children (ordered collection of `Node`): subtrees
        source (text, optional): path to file from which this todos were read

    Note:
        `Node` doesn't depend on that it stores `Todoitem`, this can be reused as
        Forest/Tree of other types of values.
    """

    def __init__(self, value=None, children=None, parent=None, source=None):
        """
        Args:
            value ()
            children (iterable of `Node`)
            parent (`Node`)
            source (text)
        """
        self._value = value
        self._parent = parent
        self._children = None
        self.set_children(children)
        self.source = source

    def __len__(self):
        return len(self.get_values())

    def __iter__(self):
        """
        Yield nodes in order from top to down.

        Imagine that this tree is in .taskpaper file,
        then nodes are yielded in order same as lines in this file.
        """
        yield self
        for child in self._children:
            for grandchild in child:
                yield grandchild

    def __add__(self, other):
        self_value, other_value = self.get_value(), other.get_value()
        if self_value and other_value:
            return Node(children=[self, other])
        elif self_value:
            return Node(children=[self] + other._children)
        elif other_value:
            return Node(children=self._children + [other])
        else:
            return Node(children=self._children + other._children)

    def iter_values(self):
        """
        Yield `Todoitem`s in order from top to down.

        Imagine that this tree is in .taskpaper file,
        then items are yielded in order same as lines in this file.
        """
        return (n.get_value() for n in self if n.get_value())

    def set_children(self, children):
        """
        Args:
            children (iterable of `Node`)
        """
        self._children = list(children) if children else []
        for c in self._children:
            c._parent = self

    def get_value(self):
        return self._value

    def get_values(self):
        return tuple(self.iter_values())

    def set_value(self, value):
        self._value = value

    def append(self, value):
        new_node = self._creat_new_node(value)
        self.append_child(new_node)

    def append_child(self, child):
        child._parent = self
        self._children.append(child)

    def prepend(self, value):
        new_node = self._creat_new_node(value)
        self.prepend_child(new_node)

    def prepend_child(self, child):
        child._parent = self
        self._children.insert(0, child)

    def _creat_new_node(self, value):
        return Node(value=value, parent=self)

    def get_parent(self):
        return self._parent

    def get_children(self):
        return self._children

    def iter_parents(self):
        node = self
        while node._parent:
            yield node._parent
            node = node._parent

    def get_parents(self):
        return tuple(self.iter_parents())

    def get_level(self):
        return len(self.get_parents())

    def iter_parents_values(self):
        return (p.get_value() for p in self.iter_parents() if p.get_value())

    def get_parents_values(self):
        return tuple(self.iter_parents_values())

    def filter(self, query):
        """
        Args:
            query (`Query`)

        Returns:
            New `Node` with only this subnodes that match query.
        """
        children_result = self._filter_children(query)
        new_node = None
        if children_result:
            new_node = Node(
                value=self.get_value(), children=children_result, source=self.source
            )
        elif query(self):
            new_node = Node(value=self.get_value(), source=self.source)
        return new_node

    def _filter_children(self, query):
        children_result_with_nones = [c.filter(query) for c in self.get_children()]
        return [c for c in children_result_with_nones if c]

    def search(self, query):
        """
        Args:
            query (`Query`)

        Returns:
            Iterator of `Todoitem`s in this `Node` that match query.
        """
        return (n.get_value() for n in self if n.get_value() and query(n))

    def find(self, value):
        """
        Args:
            value (`Todoitem`)
        Returns
            `Node` that contains given value.
        """
        for node in self:
            if node.get_value() == value:
                return node

    def append_child_to_node_with_value(self, new_value, value):
        """Returns new Node"""
        def append(node, new_value):
            return list(node.get_children()) + [Node(value=new_value)]
        return self.change_children_of_node_with_value(new_value, value, append)

    def prepend_child_to_node_with_value(self, new_value, value):
        """Returns new Node"""
        def append(node, new_value):
            return [Node(value=new_value)] + list(node.get_children())
        return self.change_children_of_node_with_value(new_value, value, append)

    def change_children_of_node_with_value(self, new_value, value, change):
        """Returns new Node"""
        v = self.get_value()
        if v == value:
            return Node(value=v, children=change(self, new_value), source=self.source)
        else:
            return Node(
                value=v,
                children=[c.change_children_of_node_with_value(new_value, value, change) for c in self.get_children()],
                source=self.source
            )
