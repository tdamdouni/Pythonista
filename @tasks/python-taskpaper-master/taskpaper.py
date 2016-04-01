"""
Created by Emil Erlandsson
Modified by Matt Dawson
Copyright (c) 2009 Matt Dawson

Rewritten by Bjoern Brandenburg
Copyright (c) 2010 Bjoern Brandenburg

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import types


def extract_tags(line):
    tags = {}

    at  = None
    arg = None

    def add_tag(at, arg, last):
        if arg:
            tags[line[at+1:arg]]  = line[arg+1:last]
        else:
            tags[line[at+1:last]] = None

    for i in xrange(len(line)):
        if line[i] == '@':
            if at is None:
                # start of a new tag
                at = i
            elif i > 0 and line[i - 1] == ' ':
                # missing closing ')' of previous argument
                add_tag(at, arg, i)
                arg = None
                at = i
        elif line[i] == ' ' and arg is None and not at is None:
            # end of a tag without an argument
            add_tag(at, arg, i)
            at = None
        elif line[i] == '(' and arg is None and not at is None:
            # start of a tag argument
            arg = i
        elif line[i] == ')' and not arg is None:
            # end of a tag with argument
            add_tag(at, arg, i)
            at  = None
            arg = None
    if not at is None:
        # last tag ends at end-of-line
        add_tag(at, arg, i)
    return tags

def indent_level(line):
    level = 0
    for i in xrange(len(line)):
        if line[i] != '\t':
            break
        level += 1
    return level


class TaskItem(object):
    """
    An entry in a TaskPaper file. Corresponds to one line.
    """

    def __init__(self, txt="", tags={}, items=None, parent=None):
        self.txt = txt.strip()
        self.parent = parent
        if not items:
            items = []
        self.items = items
        self.tags = tags
        assert parent != self
        if parent:
            parent.add_item(self)

    @staticmethod
    def parse(line, parent=None):
        tag_start = line.find('@')
        if tag_start != -1:
            tags = extract_tags(line[tag_start:])
            return TaskItem(line[:tag_start], tags=tags, parent=parent)
        else:
            return TaskItem(line, parent=parent)

    def add_item(self, item):
        self.items.append(item)

    def is_task(self):
        return self.txt.startswith('- ')

    def is_project(self):
        return self.txt.endswith(':') and not self.is_task()

    def is_note(self):
        return not (self.is_task() or self.is_project())

    def delete(self):
        "Remove node from parent's item list."
        if self.parent:
            self.parent.items.remove(self)

    def level(self):
        "Count how far this node is removed from the top level"
        count = -1
        cur = self
        while cur.parent:
            count += 1
            cur = cur.parent
        return count

    def add_tag(self, tag, value=None):
        self.tags[tag] = value

    def drop_tag(self, tag):
        if tag in self.tags:
            del self.tags[tag]
            return True
        else:
            return False

    def format(self, with_tabs=True):
        tag_txt  = " ".join(['@%s' % x if self.tags[x] is None else "@%s(%s)" % (x, self.tags[x])
                             for x in self.tags])
        tabs_txt = '\t' * self.level() if with_tabs else ''
        return "%s%s%s%s" % (tabs_txt, self.txt, ' ' if tag_txt else '', tag_txt)

    def __str__(self):
        return self.format(False)


class TaskPaper(object):
    """
    A wrapper class for TaskPaper files.
    """

    def __init__(self):
        self.items  = []
        self.parent = None

    @staticmethod
    def parse(lines):
        tp = TaskPaper()
        last_level = -1
        last_item  = tp
        for line in lines:
            level = indent_level(line)
            if level == last_level:
                # sibling
                last_item = TaskItem.parse(line, last_item.parent)
            elif level > last_item:
                # sub-item
                last_item = TaskItem.parse(line, last_item)
            else:
                # go back up
                last_item = TaskItem.parse(line, tp.last_item(level - 1))
            last_level = level
        return tp

    def add_item(self, item):
        self.items.append(item)

    def level(self):
        return 0

    def last_item(self, level=0):
        item = self
        while level >= 0:
            level -= 1
            if item.items:
                item = item.items[-1]
            else:
                break
        return item

    def select(self, predicate):
        "Iterate over all items, yield only those that match the predicate."
        to_visit = []
        to_visit.extend(reversed(self.items))
        while to_visit:
            item = to_visit.pop()
            to_visit.extend(reversed(item.items))
            assert not item in item.items
            if predicate(item):
                yield item

    def __getitem__(self, key):
        # does it look like a string?
        if isinstance(key, types.StringTypes):
            # filter by tags
            return self.select(lambda nd: key in nd.tags)
        else:
            # assume it's an index
            return self.items[key]

    def __iter__(self):
        "Iterate over all items."
        return self.select(lambda _: True)

    def format(self, predicate=None, show_parents=True):
        if predicate:
            to_show = set()
            for nd in self.select(predicate):
                to_show.add(nd)
                if show_parents:
                    while nd.parent:
                        to_show.add(nd.parent)
                        nd = nd.parent
            return "\n".join([nd.format(True)
                              for nd in self.select(lambda nd: nd in to_show)])
        else:
            return "\n".join([nd.format(True) for nd in self])

    def __str__(self):
        return self.format()
