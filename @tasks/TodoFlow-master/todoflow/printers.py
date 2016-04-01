"""Printers that can be used to output `Todos` in several formats."""

from __future__ import unicode_literals
import datetime as dt
import bisect

from . import colors
from . import textutils as tu
from . import config


class AbstractPrinter(object):
    """Implements basic structure of Printer,
    so other printers that inherit from it can only implement:

    - `format_task_text`
    - `format_project_text`
    - `format_note_text`
    - `format_empty_line_text`

    or

    - `convert_task`
    - `convert_project`
    - `convert_note`
    - `convert_empty_line`

    `format_..._text` methods receive only text of item
    `convert_...` methods receive item and optionally node that contains it

    """
    indention = config.indention

    def __call__(self, todos_tree):
        self.pprint(todos_tree)

    def pprint(self, todos_tree):
        print(self.str(todos_tree))

    def str(self, todos_tree):
        return self.unicode(todos_tree).encode('utf-8')

    def unicode(self, todos_tree):
        todos_tree = self._eject_tree(todos_tree)
        return '\n'.join(self.convert_to_list(todos_tree))

    def _eject_tree(self, todos_tree):
        try:
            return todos_tree._todos_tree
        except AttributeError:
            return todos_tree

    def convert_to_list(self, todos_tree):
        converted_nodes = [self.convert_node(n) for n in todos_tree]
        return [n for n in converted_nodes if n is not None]

    def convert_node(self, node):
        item = node.get_value()
        if item:
            return self.convert_item(item, node)

    def convert_item(self, item, node=None):
        if item.is_task:
            converted = self.convert_task(item, node)
        elif item.is_project:
            converted = self.convert_project(item, node)
        elif item.is_note:
            converted = self.convert_note(item, node)
        elif item.is_empty_line:
            converted = self.convert_empty_line(item, node)
        else:
            return None
        if converted is not None:
            return self.make_indent(item, node) + converted

    def convert_task(self, item, node=None):
        return self.format_task_text(item.text)

    def convert_project(self, item, node=None):
        return self.format_project_text(item.text)

    def convert_note(self, item, node=None):
        return self.format_note_text(item.text)

    def make_indent(self, item, node):
        if item.is_empty_line:
            return ''
        indent_level = (len(node.get_parents_values())) if node else 0
        return self.indention * indent_level

    def convert_empty_line(self, item, node=None):
        return self.format_empty_line_text(item.text)

    def format_task_text(self, text):
        raise NotImplemented()

    def format_project_text(self, text):
        raise NotImplemented()

    def format_empty_line_text(self, text):
        raise NotImplemented()

    def format_note_text(self, text):
        raise NotImplemented()


class PlainPrinter(AbstractPrinter):
    """Basic printer that converts todos to plain text in .taskpaper format."""
    def format_task_text(self, text):
        return '- ' + text

    def format_project_text(self, text):
        return text + ':'

    def format_empty_line_text(self, text):
        return ''

    def format_note_text(self, text):
        return text


class ColorPrinter(PlainPrinter):
    """Printer that converts todos to colorful text in .taskpaper format.

    Colors with ANSI escape codes.
    """
    special_tags_colors = (
        ('due', colors.ON_RED),
        ('next', colors.ON_BLUE),
        ('working', colors.ON_GREEN),
        ('today', colors.ON_GREEN),
        ('date', colors.ON_MAGENTA),
        ('in', colors.GRAY),
    )
    whole_line_tags_colors = (
        ('done', colors.GRAY),
        ('blocked', colors.YELLOW),
        ('waiting', colors.YELLOW),
    )
    tag_color = colors.YELLOW
    project_color = colors.BLUE

    def __init__(
        self,
        special_tags_colors=None,
        whole_line_tags_colors=None,
        tag_color=None,
        project_color=None,
        indention=None,
    ):
        """
        Args:
            special_tags_colors (iterable of (tag, color_code)):
                highlight special tags by assigning them unique color
                (default: specified in class)

            whole_line_tags_colors (iterable of (tag, color_code)):
                highlight whole lines that are tagged with some tag
                (default: specified in class)

            tag_color (color_code):
                highlight rest of the tags with this color
                (default: specified in class)

            project_color (color_code):
                highlight project with this color
                (default: specified in class)

            indent (text):
                indent lines using this text, default - '\\t' can be too wide
                in some terminal settings
        """
        self.special_tags_colors = special_tags_colors or self.special_tags_colors
        self.whole_line_tags_colors = whole_line_tags_colors or self.whole_line_tags_colors
        self.tag_color = tag_color or self.tag_color
        self.project_color = project_color or self.project_color
        self.special_tags = [t[0] for t in self.special_tags_colors]
        self.indention = indention or self.indention

    def format_project_text(self, text):
        return super(ColorPrinter, self).format_project_text(
            self.project_color + text + colors.DEFAULT
        )

    def convert_task(self, item, node):
        whole_line_colored = self._handle_whole_line_tags(item)
        if whole_line_colored:
            return self.format_task_text(whole_line_colored)
        text = self.handle_special_tags(item.text)
        text = self.handle_rest_of_tags(text)
        return self.format_task_text(text)

    def _handle_whole_line_tags(self, item):
        for tag, color in self.whole_line_tags_colors:
            if item.has_tag(tag):
                return color + item.text + colors.DEFAULT

    def handle_special_tags(self, text):
        return self.colorize_tags(text, self.special_tags_colors)

    def handle_rest_of_tags(self, text):
        rest_of_tags = self.get_rest_of_tags(text)
        return self.colorize_tags(text, [(t, self.tag_color) for t in rest_of_tags])

    def get_rest_of_tags(self, text):
        tags_from_text = tu.get_all_tags(text)
        return [t for t in tags_from_text if t not in self.special_tags]

    def colorize_tags(self, text, tags_colors):
        for tag, color in tags_colors:
            text = tu.enclose_tag(text, tag, color, colors.DEFAULT)
        return text


class CountdownPrinter(AbstractPrinter):
    """Converts todos to colorful text representation in form:

    <time_left> item title @<countdown_tag>(<when_is_due>) [items of whisc this item is subitem]

    """
    countdown_tag_color = colors.MAGENTA
    time_left_ranges = (
        dt.timedelta(days=1),
        dt.timedelta(days=2),
        dt.timedelta(days=7),
        dt.timedelta(days=14),
    )
    time_left_colors = (
        colors.on_red,
        colors.red,
        colors.yellow,
        colors.blue,
        colors.green,
    )

    def __init__(
        self, countdown_tag, countdown_tag_color=None,
        time_left_ranges=None, time_left_colors=None,
    ):
        """
        Args:
            countdown_tag (text): Only items with this tag will be displayed.
                Must have parameter with date in form 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD'.

            countdown_tag_color (color_code):
                Color to highlight `countdown_tag`.

            time_left_ranges (list of timedelta):
                Time left have color assigned based on range in which it is contained.

            time_left_colors (list of color function):
                Color to highlight time left in corresponding range. Must have lenght greated
                than `time_left_ranges`.


        """
        self.countdown_tag = countdown_tag
        self.countdown_tag_color = countdown_tag_color or self.countdown_tag_color
        self.time_left_ranges = time_left_ranges or self.time_left_ranges
        self.time_left_colors = time_left_colors or self.time_left_colors
        self.now = dt.datetime.now()

    def unicode(self, todos_tree):
        todos_tree = self._eject_tree(todos_tree)
        times_and_texts = self.convert_to_list(todos_tree)
        times_and_texts.sort()
        return '\n'.join([t[1] for t in times_and_texts])

    def convert_item(self, item, node):
        if item.has_tag(self.countdown_tag):
            return self.format_item(
                item,
                node.get_parents_values(),
            )

    def format_item(self, item, parents):
        time_left = self.calculate_time_left(item)
        time_left_text = self.format_time_left(time_left)
        text = self.format_text(item.text)
        parents_text = self.format_parents(parents)
        return (time_left, '{} {} {}'.format(time_left_text, text, parents_text))

    def calculate_time_left(self, item):
        countdown_date = self.parse_date_from_tag(item, self.countdown_tag)
        return countdown_date - self.now

    def format_time_left(self, time_left):
        color = self.find_color(time_left)
        return color('{:02d} {:02d}:{:02d}'.format(
            time_left.days,
            time_left.seconds / 3600,
            (time_left.seconds % 3600) / 60
        ))

    def find_color(self, time_left):
        index = bisect.bisect(self.time_left_ranges, time_left)
        return self.time_left_colors[index]

    def parse_date_from_tag(self, item, tag):
        return tu.parse_datetime(item.get_tag_param(tag))

    def format_parents(self, parents):
        return colors.gray(
            ' / '.join([p.text for p in parents])
        )

    def format_text(self, text):
        return tu.enclose_tag(
            text, self.countdown_tag, self.countdown_tag_color, colors.DEFAULT
        )


pprint = PlainPrinter().pprint
