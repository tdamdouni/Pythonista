from __future__ import unicode_literals

import unittest
import datetime as dt

import todoflow.textutils as tu


class TestTypes(unittest.TestCase):
    def text(self, text):
        self._text = text
        return self

    def is_task(self):
        self.assertTrue(tu.is_task(self._text))
        return self

    def isnt_task(self):
        self.assertFalse(tu.is_task(self._text))
        return self

    def is_project(self):
        self.assertTrue(tu.is_project(self._text))
        return self

    def isnt_project(self):
        self.assertFalse(tu.is_project(self._text))
        return self

    def is_note(self):
        self.assertTrue(tu.is_note(self._text))
        return self

    def isnt_note(self):
        self.assertFalse(tu.is_note(self._text))
        return self

    def test_task(self):
        self.text('- something to do').is_task().isnt_project().isnt_note()

    def test_indented_task(self):
        self.text('\t\t- some task').is_task().isnt_project().isnt_note()

    def test_task_with_color(self):
        self.text('- some task:').is_task().isnt_project().isnt_note()

    def test_project(self):
        self.text('some project:').is_project().isnt_task().isnt_note()

    def test_indented_project(self):
        self.text('\t\t\tsome project:').is_project().isnt_task().isnt_note()

    def test_note(self):
        self.text('\t\t\tsome note').is_note().isnt_task().isnt_project()


class TestTags(unittest.TestCase):
    def text(self, text):
        self._text = text
        return self

    def has_tag(self, tag):
        self.assertTrue(tu.has_tag(self._text, tag))
        self.tag = tag
        return self

    def doesnt_have_tag(self, tag):
        self.assertFalse(tu.has_tag(self._text, tag))
        self.tag = tag
        return self

    def with_param(self, param):
        self.assertEqual(tu.get_tag_param(self._text, self.tag), param)
        return self

    def with_tag(self, tag):
        self.tag = tag
        return self

    def removed(self):
        self._text = tu.remove_tag(self._text, self.tag)
        return self

    def added(self, with_param=None):
        self._text = tu.add_tag(self._text, self.tag, param=with_param)
        return self

    def replaced_by(self, replacement):
        self._text = tu.replace_tag(self._text, self.tag, replacement)
        return self

    def enclosed_by(self, prefix, suffix=None):
        self._text = tu.enclose_tag(self._text, self.tag, prefix, suffix)
        return self

    def is_equal(self, text):
        self.assertEqual(self._text, text)
        return self

    def has_tags(self, *args):
        text_tags = set(tu.get_all_tags(self._text))
        self.assertEqual(text_tags, set(args))
        return self

    def param_modified_by(self, modificaiton):
        self._text = tu.modify_tag_param(self._text, self.tag, modificaiton)
        return self

    def toggled(self, tags):
        self._text = tu.toggle_tags(self._text, tags)
        return self


class TestTagsFinding(TestTags):
    def test_tag_with_at(self):
        self.text('- same text @done rest of text').has_tag('@done')

    def test_tag_at_end(self):
        self.text('- some text with @done').has_tag('@done')

    def test_tag_without_at(self):
        self.text('- some text @today rest').has_tag('today')

    def test_tag_at_beggining(self):
        self.text('@done rest').has_tag('@done')

    def test_tag_with_param(self):
        self.text('some text @start(2014-01-01) rest').has_tag('@start')

    def test_doesnt_have(self):
        self.text('some text @tag2 rest').doesnt_have_tag('tag')

    def test_get_tag_param(self):
        self.text('some txet @tag(2) rest').has_tag('@tag').with_param('2')

    def test_get_tag_param_at_end(self):
        self.text('some txet @done(01-14)').has_tag('@done').with_param('01-14')

    def test_empty_param(self):
        self.text('@empty()').has_tag('empty').with_param('')

    def test_no_param(self):
        self.text('@no_param').has_tag('@no_param').with_param(None)

    def test_no_tag(self):
        self.text('text without tag').doesnt_have_tag('@test').with_param(None)

    def test_succeeding_tag(self):
        self.text('text @tag1(yo) @tag2(wo) rest').has_tag('@tag1').with_param('yo')

    def test_get_all_tags(self):
        self.text('text @today @working test @done').has_tags('today', 'working', 'done')

    def test_get_all_tags_with_params(self):
        self.text('text @today(!) @working test @done(2014-01-10)').has_tags('today', 'working', 'done')

    def test_toggle_tags(self):
        now = dt.datetime.now()
        tags = [('next', None), ('working', None), ('done', '%Y-%m-%d')]
        self.text('text').toggled(tags).is_equal('text @next')
        self.toggled(tags).is_equal('text @working')
        self.toggled(tags).is_equal(now.strftime('text @done(%Y-%m-%d)'))
        self.toggled(tags).is_equal('text')


class TestTagsRemoving(TestTags):
    def test_remove_tag(self):
        self.text('text @done rest').with_tag('@done').removed().is_equal('text rest')

    def test_remove_tag_without_at(self):
        self.text('text @today rest').with_tag('today').removed().is_equal('text rest')

    def test_remove_tag_with_param(self):
        self.text('text @start(2014) rest').with_tag('start').removed().is_equal('text rest')

    def test_remove_tag_at_end(self):
        self.text('text @start(2014)').with_tag('start').removed().is_equal('text')


class TestTagsReplacing(TestTags):
    def test_replace_tag(self):
        self.text('text @tag rest').with_tag('@tag').replaced_by('sub').is_equal('text sub rest')

    def test_replace_tag_with_param(self):
        self.text('text @tag(1) rest').with_tag('tag').replaced_by('sub').is_equal('text sub rest')


class TestTagsAdding(TestTags):
    def test_add_tag(self):
        self.text('some text').with_tag('@today').added().is_equal('some text @today')

    def test_add_tag_without_at(self):
        self.text('some text').with_tag('today').added().is_equal('some text @today')

    def test_add_tag_with_param(self):
        self.text('yo').with_tag('@done').added(with_param='01-10').is_equal('yo @done(01-10)')

    def test_add_tag_with_not_text_param(self):
        self.text('meaning').with_tag('@of').added(with_param=42).is_equal('meaning @of(42)')

    def test_add_tag_with_exisiting_tag(self):
        self.text('text @t(9)').with_tag('@t').added().is_equal('text @t')


class TestTagsEnclosing(TestTags):
    def test_enclose_tag(self):
        self.text('text @done rest').with_tag('@done').enclosed_by('**').is_equal('text **@done** rest')

    def test_enclose_tag_with_suffix(self):
        self.text('text @start rest').with_tag('@start').enclosed_by('<', '>').is_equal('text <@start> rest')

    def test_enclose_tag_with_param(self):
        self.text('tx @in(01-01) rt').with_tag('@in').enclosed_by('**').is_equal('tx **@in(01-01)** rt')

    def test_enclode_tag_at_end(self):
        self.text('tx @in(01-01)').with_tag('@in').enclosed_by('*').is_equal('tx *@in(01-01)*')


class TestTagsParamsModifing(TestTags):
    def test_modify_tag_param(self):
        self.text('tx @t(1) rt').with_tag('t').param_modified_by(lambda p: int(p) + 1).is_equal('tx @t(2) rt')

    def test_modify_tag_param_without_param(self):
        self.text('tx @t(x) rt').with_tag('t').param_modified_by(
            lambda p: p * 2 if p else 'y'
        ).is_equal('tx @t(xx) rt')
        self.text('tx @t rt').with_tag('t').param_modified_by(
            lambda p: p * 2 if p else 'y'
        ).is_equal('tx @t(y) rt')


class TestSortingByTag(unittest.TestCase):
    def shuffled_texts(self, *args):
        from random import shuffle
        args_list = list(args)
        shuffle(args_list)
        self._texts = tuple(args_list)
        return self

    def sorted_by(self, tag, reverse=False):
        self._texts = tu.sort_by_tag_param(self._texts, tag, reverse)
        return self

    def are_equal(self, *args):
        self.assertEqual(self._texts, tuple(args))
        return self

    def test_sort_by_tag(self):
        list1 = 'yo', 'yo @t(1)', '@t(2) @k(1000)', 'fd @t(4)'
        self.shuffled_texts(*list1).sorted_by('t').are_equal(*list1)

    def test_sort_by_tag_reversed(self):
        list1 = 'yo', 'yo @t(1)', '@t(2) @k(1000)', 'fd @t(4)'
        self.shuffled_texts(*list1).sorted_by('t', reverse=True).are_equal(*list1[::-1])


class TestFormatters(unittest.TestCase):
    def text(self, text):
        self._text = text
        return self

    def with_stripped_formatting_is(self, text):
        self._text = tu.strip_formatting(self._text)
        self.assertEqual(self._text, text)
        return self

    def indention_level_is(self, level):
        self.assertEqual(tu.calculate_indent_level(self._text), level)

    def with_stripped_formatting_and_tags_is(self, text):
        self._text = tu.strip_formatting_and_tags(self._text)
        self.assertEqual(self._text, text)
        return self

    def test_strip_task(self):
        self.text('\t\t- text').with_stripped_formatting_is('text')

    def test_strip_ignore_spaces(self):
        self.text('\t\t  text').with_stripped_formatting_is('  text')

    def test_strip_task_with_colon(self):
        self.text('\t\t- text:').with_stripped_formatting_is('text:')

    def test_strip_project(self):
        self.text('\ttext:').with_stripped_formatting_is('text')

    def test_strip_note(self):
        self.text('\ttext\t').with_stripped_formatting_is('text')

    def test_strip_tags(self):
        self.text('\ttext @done rest @today').with_stripped_formatting_and_tags_is('text rest')

    def test_calculate_indent_level_0(self):
        self.text('text').indention_level_is(0)

    def test_calculate_indent_level_1(self):
        self.text('\ttext').indention_level_is(1)

    def test_calculate_indent_level_5(self):
        self.text('\t\t\t\t\ttext').indention_level_is(5)

    def test_calculate_indent_ignore_spaces(self):
        self.text('  text').indention_level_is(0)

    def test_calculate_indent_ignore_tab_after_spaces(self):
        self.text('  \ttext').indention_level_is(0)

    def test_calculate_indent_ignore_spaces_after_tab(self):
        self.text('\t  text').indention_level_is(1)


class TestParseDate(unittest.TestCase):
    def parsing(self, text):
        self.date = tu.parse_datetime(text)
        return self

    def gives(self, year, month, day, hour, minute):
        self.assertEqual(self.date.year, year)
        self.assertEqual(self.date.month, month)
        self.assertEqual(self.date.day, day)
        self.assertEqual(self.date.hour, hour)
        self.assertEqual(self.date.minute, minute)

    def test_parse_datetime_hour_with_leading_zero(self):
        self.parsing('2014-11-01 08:45').gives(2014, 11, 1, 8, 45)

    def test_parse_datetime_hour_without_leading_zero(self):
        self.parsing('2014-11-01 8:45').gives(2014, 11, 1, 8, 45)

    def test_parse_without_time(self):
        self.parsing('2014-11-01').gives(2014, 11, 1, 0, 0)


if __name__ == '__main__':
    unittest.main()
