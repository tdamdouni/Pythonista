from __future__ import absolute_import

from . import textutils as tu
from .printers import PlainPrinter
from .compatibility import unicode, _str_


class Todoitem(object):
    """Representation of single todo item.

    It can be task, project or note.

    Note:
        `Todoitem` knows nothing about it's place in whole todos.
        (For example it doesn't know which other item contains it)
    """
    _uniqueid_counter = 0

    @classmethod
    def from_text(cls, text):
        return Todoitem(text)

    @classmethod
    def from_token(cls, token):
        item = Todoitem(token.text)
        item.linenum = token.linenum
        item.start = token.start
        item.end = token.end
        return item

    @classmethod
    def _gen_uniqueid(cls):
        cls._uniqueid_counter += 1
        return unicode(cls._uniqueid_counter)

    def __init__(self, text=''):
        """Creates `Todoitem` from text."""
        # internally text of todoitem is stored in stripped form
        # without '\t' indent,  task indicator - '- ',
        # and project indicator ':'
        self.uniqueid = self._gen_uniqueid()
        self.text = tu.strip_formatting(text) if text else ''
        self._choose_type(text)
        self.linenum = None

    def __unicode__(self):
        return PlainPrinter().convert_item(self)

    def __str__(self):
        return _str_(self)

    def __repr__(self):
        return '<Todoitem: {} | "{}" | {}>'.format(
            self.uniqueid, self.text, self.get_type_name()
        )

    def _choose_type(self, text):
        self._set_all_types_flags_to_false()
        if not text:
            self.is_empty_line = True
        elif tu.is_task(text):
            self.is_task = True
        elif tu.is_project(text):
            self.is_project = True
        else:
            self.is_note = True

    def _set_all_types_flags_to_false(self):
        self.is_task = False
        self.is_project = False
        self.is_note = False
        self.is_empty_line = False

    def get_type_name(self):
        types = ('project', 'note', 'task', 'empty_line')
        for type_name in types:
            if getattr(self, 'is_' + type_name):
                return type_name
        return 'no_type?'

    def tag(self, tag_to_use, param=None):
        self.text = tu.add_tag(self.text, tag_to_use, param)

    def remove_tag(self, tag_to_remove):
        self.text = tu.remove_tag(self.text, tag_to_remove)

    def has_tag(self, tag):
        return tu.has_tag(self.text, tag)

    def get_tag_param(self, tag):
        return tu.get_tag_param(self.text, tag)

    def edit(self, new_text):
        self.text = tu.strip_formatting(new_text)

    def change_to_task(self):
        self._set_all_types_flags_to_false()
        self.is_task = True

    def change_to_project(self):
        self._set_all_types_flags_to_false()
        self.is_project = True

    def change_to_note(self):
        self._set_all_types_flags_to_false()
        self.is_note = True

    def change_to_empty_line(self):
        self._set_all_types_flags_to_false()
        self.is_empty_line = True
