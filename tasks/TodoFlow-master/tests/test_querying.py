# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Ugly indentation of """ """ strings that is breaking pep8
# is this way because this
# is imo more readable than alternatives in this particular case

import unittest

import todoflow
from todoflow.querying_parser import parse as parse_query
from todoflow.parser import parse as parse_todos
from todoflow.compatibility import unicode


class TestQuering(unittest.TestCase):
    def query(self, query):
        self._query = parse_query(query)
        return self


class TestQueriesBasedOnText(TestQuering):
    def matches(self, text):
        self.assertTrue(self._query.matches_text(text))
        return self

    def doesnt_match(self, text):
        self.assertFalse(self._query.matches_text(text))
        return self


class TestTextAndTag(TestQueriesBasedOnText):
    def test_text(self):
        self.query(
            'some text'
        ).matches(
            'something before some text something after'
        ).doesnt_match(
            'sometext ome text'
        )

    def test_tag(self):
        self.query(
            '@done'
        ).matches(
            '- text @done rest'
        ).doesnt_match(
            '- text'
        )


class TestArgumentOperators(TestQueriesBasedOnText):
    def test_tag_eq(self):
        self.query(
            '@done = 2014-02-10'
        ).matches(
            '- text @done(2014-02-10) rest'
        ).doesnt_match(
            '- text @done(2014-02-11)'
        ).doesnt_match(
            '- text'
        )

    def test_tag_neq(self):
        self.query(
            '@done != 2014-02-10'
        ).doesnt_match(
            '- text @done(2014-02-10) rest'
        ).matches(
            '- text @done(2014-02-11)'
        ).doesnt_match(
            '- text'
        )

    def test_tag_lt(self):
        self.query(
            '@done < 2014-02-10'
        ).matches(
            '- text @done(2014-02-09) rest'
        ).doesnt_match(
            '- text @done(2014-02-11)'
        ).doesnt_match(
            '- text'
        )

    def test_tag_gte(self):
        self.query(
            '@done >= 2014-02-10'
        ).matches(
            '- text @done(2014-02-10) rest'
        ).matches(
            '- text @done(2014-03-11) rest'
        ).doesnt_match(
            '- text @done(2014-02-09)'
        ).doesnt_match(
            '- text'
        )

    def test_tag_contains(self):
        self.query(
            '@persons <- John'
        ).matches(
            '- text @persons(John, Terry)'
        ).doesnt_match(
            '@persons(Terry, Eric)'
        )

    def test_tag_in(self):
        self.query(
            '@person -> John, Eric, Graham, Michael'
        ).matches(
            '- text @person(John)'
        ).doesnt_match(
            '- text @person(Terry)'
        )


class TestLogicalOperators(TestQueriesBasedOnText):
    def test_and(self):
        self.query(
            'A and B'
        ).matches(
            'A B C'
        ).doesnt_match(
            'A C'
        ).doesnt_match(
            'C D E'
        ).doesnt_match(
            'D E B'
        )

    def test_or(self):
        self.query(
            'A or B'
        ).matches(
            'A C B'
        ).matches(
            'A C D'
        ).matches(
            'D E B'
        ).doesnt_match(
            'E RT'
        )

    def test_not(self):
        self.query(
            'not A'
        ).doesnt_match('DEFAQ').matches('DFQ')

    def test_parenthesis(self):
        self.query(
            '(A or B) and C'
        ).matches('AC').matches('BC').doesnt_match('AB')


class TestParenthesis(TestQueriesBasedOnText):
    def test_parsing_tag(self):
        self.assertTrue(parse_query('@start'))

    def test_parsing_tag_or(self):
        self.assertTrue(parse_query('@start <= 2015-06-25 or not @start'))

    def test_parsing_text_in_paren(self):
        self.assertTrue(parse_query('(a)'))

    def test_parsing_text_or_in_paren(self):
        self.assertTrue(parse_query('(a or b)'))

    def test_parsing_text_or_in_paren_or(self):
        self.assertTrue(parse_query('(a or b) or c'))

    def test_parsing_text_or_in_paren_or_tag(self):
        self.assertTrue(parse_query('(a or b) or @c'))

    def test_parsing_tag_in_paren(self):
        self.assertTrue(parse_query('(@a)'))

    def test_parsing_tag_or_in_paren(self):
        self.assertTrue(parse_query('(@a or b)'))

    def test_parsing_tag_or_tag_in_paren(self):
        self.assertTrue(parse_query('(@a or @b)'))

    def test_parsing_tag_or_tag(self):
        self.assertTrue(parse_query('@a or @b'))

    def test_hide_not_started_query(self):
        self.query(
            '((@start <= 2015-06-25 or not @start) and not @done)'
        ).matches('A')


class TestPlusD(TestQueriesBasedOnText):
    def test_plus_d(self):
        self.assertTrue(parse_query('a +d'))

    def test_parens_plus_d(self):
        self.assertTrue(parse_query('a or b +d'))
        self.assertTrue(parse_query('a and b +d'))


class TestParsedTodos(unittest.TestCase):
    def todos(self, text):
        self._todos = parse_todos(text)
        return self

    def with_source_mocked_to(self, path):
        self._todos.set_source(path)
        return self


class TestFiltering(TestParsedTodos):
    def filtered_by(self, query):
        self._todos = self._todos.filter(query)
        return self

    def are(self, text):
        self.assertEqual(unicode(self._todos), text)
        return self

    def test_text(self):
        self.todos(
"""project:
\t- subtask
"""
        ).filtered_by('subtask').are(
"""project:
\t- subtask"""
        )

    def test_project(self):
        self.todos(
"""A:
\t- 1
\t- 2

B:
\t- 3
\t- 4"""
        ).filtered_by('project = A').are(
"""A:
\t- 1
\t- 2"""
        )

    def test_type(self):
        self.todos(
"""A:
\t- 1
\t- 2

B:"""
        ).filtered_by('type = "project"').are(
"""A:
B:"""
        )

    def test_plus_descendant(self):
        self.todos(
"""A:
\t- 1
\t\t- 2
B:
\t- 3
\t- 4
"""
        ).filtered_by('A +d').are(
"""A:
\t- 1
\t\t- 2"""
        )

    def test_only_first(self):
        self.todos(
"""A:
\t- 1 @done
\t- 2 @done
\t- 3
\t- 4
\t- 5"""
        ).filtered_by('not @done +f').are(
"""A:
\t- 3"""
        )

    def test_deep_only_first(self):
        self.todos(
"""A:
\t- 1 @done
\t- 2 @done
\t- 3
\t- 4
\t- 5
\t\t- 5a @done
\t\t- 5b
\t\t- 5c
\t- 6"""
        ).filtered_by('not @done +f').are(
"""A:
\t- 3
\t- 5
\t\t- 5b"""
        )

    def test_linenum_start(self):
        self.todos(
"""- 0
- 1
- 2
"""
        ).filtered_by('linenum = 0').are(
"""- 0"""
        )

    def test_linenum_middle(self):
        self.todos(
"""- 0
- 1
2:
\t- 3
4
"""
        ).filtered_by('linenum = 3').are(
"""2:
\t- 3"""
        )

    def test_source_when_none(self):
        self.todos(
"""- 0
- 1"""
        ).filtered_by('source = Task.taskpaper').are(
""""""
        )

    def test_plus_d_and_type(self):
        self.todos(
"""Project:
\t- Task 1
""").filtered_by('not @done and type = task +d').are(
"""Project:
\t- Task 1"""
)

    def test_source(self):
        self.todos(
"""p:
\t- 1
\t\t- 2
- 3"""
        ).with_source_mocked_to('Task.taskpaper').filtered_by('source = Task.taskpaper').are(
"""p:
\t- 1
\t\t- 2
- 3"""
        )


class TestSearching(TestFiltering):
    def searched_by(self, query):
        self.search_results = tuple(
            (i.text for i in self._todos.search(query))
        )
        return self

    def are_giving(self, results):
        self.assertEqual(self.search_results, results)
        return self

    def test_text(self):
        self.todos(
"""A:
\t- 1 b
\t- 2 b
\t- 3
\t\t- 4 b"""
        ).searched_by('b').are_giving(
            ('1 b', '2 b', '4 b')
        ).searched_by('3').are_giving(
            ('3', )
        )

    def test_plus_descendant(self):
        self.todos(
"""A:
\t- 1 @done
\t- 2 @done
\t- 3
\t- 4
\t- 5 @done
\t\t- 5a
\t\t- 5b
\t\t- 5c
\t- 6"""
        ).searched_by('@done +d').are_giving(
            ('1 @done', '2 @done', '5 @done', '5a', '5b', '5c')
        )

    def test_only_first(self):
        self.todos(
"""A:
\t- 1 @done
\t- 2 @done
\t- 3
\t- 4
\t- 5 @done
\t\t- 5a
\t\t- 5b
\t\t- 5c
\t- 6"""
        ).searched_by('not @done +f').are_giving(
            ('A', '3', '5a')
        )


if __name__ == '__main__':
    unittest.main()
