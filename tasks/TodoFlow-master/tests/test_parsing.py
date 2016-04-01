from __future__ import unicode_literals
# Ugly indentation of """ """ strings that is breaking pep8
# is this way because this
# is imo more readable than alternatives in this particular case

import unittest

import todoflow.lexer as lexer
import todoflow.parser as parser
import todoflow.config
from todoflow.compatibility import *


class TestLexer(unittest.TestCase):
    def tokens_from(self, text):
        self.tokens = lexer.Lexer(text).tokens
        return self

    def are(self, expected_tokens_repr):
        tokens_repr = ''.join([t.tok() for t in self.tokens])
        self.assertEqual(tokens_repr, expected_tokens_repr)
        return self

    def test_tokens(self):
        self.tokens_from(
"""1
2
3"""
        ).are('***$')

    def test_tokens_width_indent(self):
        self.tokens_from(
"""1
\t2
3"""
        ).are('*>*<*$')

    def test_tokens_with_continuos_indent(self):
        self.tokens_from(
"""1
\t2
\t3
\t4"""
        ).are('*>***$')

    def test_tokens_with_varying_indent(self):
        self.tokens_from(
"""1
\t2
\t\t3
\t4"""
        ).are('*>*>*<*$')

    def test_tokens_with_empty_line(self):
        self.tokens_from(
"""1

2"""
        ).are('*n*$')

    def test_tokens_with_empty_line_at_end(self):
        self.tokens_from(
"""1
2
"""
        ).are('**n$')


class TestParser(unittest.TestCase):
    def todos_from(self, text):
        self.todos = parser.parse(text)
        self.nodes = list(self.todos._todos_tree)
        return self

    def main_node(self):
        return self.node(0)

    def first_node(self):
        return self.node(1)

    def second_node(self):
        return self.node(2)

    def third_node(self):
        return self.node(3)

    def node(self, index):
        self._node = self.nodes[index]
        return self

    def is_task(self):
        self.assertTrue(self._node.get_value().is_task)
        return self

    def is_project(self):
        self.assertTrue(self._node.get_value().is_project)
        return self

    def is_note(self):
        self.assertTrue(self._node.get_value().is_note)
        return self

    def has_subtasks(self, howmany):
        self.assertEqual(len(self._node.get_children()), howmany)
        return self

    def doesnt_have_item(self):
        self.assertEqual(self._node.get_value(), None)
        return self

    def test_single_task(self):
        self.todos_from(
"""- task"""
        ).first_node().is_task().has_subtasks(0)

    def test_single_project(self):
        self.todos_from(
"""project:"""
        ).first_node().is_project().has_subtasks(0)

    def test_single_note(self):
        self.todos_from(
"""note"""
        ).first_node().is_note().has_subtasks(0)

    def test_simple_subtasks(self):
        self.todos_from(
"""project:
\t- task1
\t- task2"""
        )
        self.main_node().doesnt_have_item()
        self.first_node().has_subtasks(2).second_node().has_subtasks(0)

    def test_tasks_at_0_level(self):
        self.todos_from(
"""- task 1
- task 2
- task 3"""
        ).main_node().doesnt_have_item().has_subtasks(3)

    def test_tasks_at_0_level_with_empty_lines(self):
        self.todos_from(
"""- task 1
- task 2

- task 3
"""
        ).main_node().doesnt_have_item().has_subtasks(5)

    def test_deep_indent(self):
        self.todos_from(
"""project:
\t- task 1
\t\t- subtask 1
\t\t\t- subsubtask 1
\t\t\t- subsubtask 2
\t\t- subtask 2
\t- task 2

"""
        )
        self.main_node().doesnt_have_item().has_subtasks(3)
        self.first_node().is_project().has_subtasks(2)
        self.second_node().is_task().has_subtasks(2)
        self.third_node().is_task().has_subtasks(2)

    def test_deep_indent_with_empty_line_in_the_middle(self):
        self.todos_from(
"""project:
\t- task 1
\t\t- subtask 1
\t\t\t- subsubtask 1

\t\t\t- subsubtask 2
\t\t- subtask 2
\t- task 2

"""
        )
        self.main_node().doesnt_have_item().has_subtasks(3)
        self.first_node().is_project().has_subtasks(2)
        self.second_node().is_task().has_subtasks(2)
        self.third_node().is_task().has_subtasks(3)


class TestPlainPrinting(unittest.TestCase):
    def text_after_parsing_is_the_same(self, text):
        todos = parser.parse(text)
        self.assertEqual(unicode(todos), text)

    def test_task(self):
        self.text_after_parsing_is_the_same(
"""- task"""
        )

    def test_project(self):
        self.text_after_parsing_is_the_same(
"""project:"""
        )

    def test_project_with_subtask(self):
        self.text_after_parsing_is_the_same(
"""project:
\t- task 1
\t- task 2"""
        )

    def test_deep_indent(self):
        self.text_after_parsing_is_the_same(
"""project:
\t- task 1
\t\t- task 2
\t\t\t- task 3"""
        )

    def test_empty_line(self):
        self.text_after_parsing_is_the_same(
"""- task 1

\t- task2
"""
        )

    def test_empty_line_at_end(self):
        self.text_after_parsing_is_the_same(
"""- task 1
\t- task2
"""
        )

    def test_empty_line_at_beginning(self):
        self.text_after_parsing_is_the_same(
"""
- task 1
\t- task2"""
        )

    def test_multiple_empty_lines_at_end(self):
        self.text_after_parsing_is_the_same(
"""- task 1
\t- task2


"""
        )

if __name__ == '__main__':
    unittest.main()
