from __future__ import absolute_import

from . import textutils as tu


class AbstractQuery(object):
    def matches(self, todonode):
        raise NotImplementedError

    def __call__(self, todonode):
        return self.matches(todonode)


# Basic
class TextQuery(AbstractQuery):
    def matches(self, todonode):
        item = todonode.get_value()
        if item:
            return self.matches_text(item.text)


class SubstringQuery(TextQuery):
    def __init__(self, text):
        self.text = text.lower()

    def matches_text(self, text):
        return self.text in text.lower()


class TagQuery(TextQuery):
    def __init__(self, tag):
        self.tag = tag

    def matches_text(self, text):
        return tu.has_tag(text, self.tag)


# Logical operators
class NotQuery(AbstractQuery):
    def __init__(self, query):
        self.query = query

    def matches(self, todonode):
        return not self.query.matches(todonode)

    def matches_text(self, text):
        return not self.query.matches_text(text)


class AbstractBinaryQuery(AbstractQuery):
    def __init__(self, query1, query2):
        self.query1 = query1
        self.query2 = query2

    def matches(self, todonode):
        return self.operation(self.query1.matches(todonode), self.query2.matches(todonode))

    def matches_text(self, text):
        return self.operation(self.query1.matches_text(text), self.query2.matches_text(text))


class AndQuery(AbstractBinaryQuery):
    operation = lambda _, a, b: a and b  # self is on first place


class OrQuery(AbstractBinaryQuery):
    operation = lambda _, a, b: a or b  # self is on first place


# ops
class TagOpQuery(TextQuery):
    def __init__(self, tag, operation=None, right_side=None):
        self.tag = tag
        self.operation = operation
        self.right_side = right_side.strip() if right_side else ''

    def matches_text(self, text):
        param = tu.get_tag_param(text, self.tag)
        if param is None:
            return False
        return self.operation(param, self.right_side)


class PredefinedLeftOpQuery(AbstractQuery):
    def __init__(self, operation=None, right_side=None):
        self.operation = operation
        self.right_side = right_side.strip() if right_side else ''


class ProjectOpQuery(PredefinedLeftOpQuery):
    def matches(self, todonode):
        for n in [todonode] + list(todonode.get_parents()):
            v = n.get_value()
            if v and v.is_project and self.operation(v.text, self.right_side):
                return True


class LinenumOpQuery(PredefinedLeftOpQuery):
    def matches(self, todonode):
        v = todonode.get_value()
        if not v:
            return False
        return self.operation(str(v.linenum), self.right_side)


class SourceOpQuery(PredefinedLeftOpQuery):
    def matches(self, todonode):
        for n in [todonode] + list(todonode.get_parents()):
            if self.operation(n.source, self.right_side):
                return True
        return False


# whole list
class PlusDescendants(AbstractQuery):
    def __init__(self, query):
        self.query = query

    def matches(self, todonode):
        for n in [todonode] + list(todonode.get_parents()):
            if self.query(n):
                return True


class OnlyFirst(AbstractQuery):
    def __init__(self, query):
        self.query = query

    def matches(self, todonode):
        if not todonode.get_parent():
            return True
        todos = todonode.get_parent()
        if not todos.get_children():
            return True
        return self._is_node_first_that_matches(todos.get_children(), todonode)

    def _is_node_first_that_matches(self, items, todonode):
        matching_items = [n for n in items if self.query.matches(n)]
        return matching_items[0] == todonode if matching_items else False


class TypeOpQuery(AbstractQuery):
    def __init__(self, operation=None, right_side=None):
        self.operation = operation
        self.right_side = right_side

    def matches(self, todonode):
        value = todonode.get_value()
        if not value:
            return False
        return {
            'task': value.is_task,
            'note': value.is_note,
            'project': value.is_project,
        }.get(self.right_side, False)


class UniqueidOpQuery(AbstractQuery):
    def __init__(self, operation=None, right_side=None):
        self.operation = operation
        self.right_side = right_side

    def matches(self, todonode):
        return self.operation(todonode.get_value().uniqueid, self.right_side)
