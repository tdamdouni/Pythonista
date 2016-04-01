from __future__ import unicode_literals

import unittest

import todoflow.todoflow as tf
import todoflow
from todoflow.compatibility import read, unicode, write


class TestTodoitem(unittest.TestCase):
    def test_task(self):
        task = todoflow.todoitem.Todoitem('- task')
        self.assertTrue(task.is_task)
        self.assertEqual('task', task.text)
        self.assertEqual('- task', unicode(task))

    def test_project(self):
        task = todoflow.todoitem.Todoitem('project:')
        self.assertTrue(task.is_project)
        self.assertEqual('project', task.text)
        self.assertEqual('project:', unicode(task))

    def test_note(self):
        task = todoflow.todoitem.Todoitem('note')
        self.assertTrue(task.is_note)
        self.assertEqual('note', task.text)
        self.assertEqual('note', unicode(task))


class TestSingleTodosFile(unittest.TestCase):
    def todos_from(self, path):
        self.source = path
        self.todos = tf.from_path(path)
        return self

    def are_same_as_in_file(self):
        original_text = read(self.source)
        new_text = unicode(self.todos)
        self.assertEqual(original_text, new_text)
        return self

    def saved_to(self, path):
        self.destintation = path
        tf.to_path(self.todos, path)
        return self

    def are_same_as_in_original_file(self):
        original_text = read(self.source)
        new_text = read(self.destintation)
        self.assertEqual(original_text, new_text)
        return self

    def test_loading_from_path(self):
        self.todos_from(
            'tests/resources/todos.taskpaper'
        ).are_same_as_in_file()

    def test_saving_to_path(self):
        self.todos_from(
            'tests/resources/todos.taskpaper'
        ).saved_to(
            'tests/resources/temp.taskpaper'
        ).are_same_as_in_original_file()


class TestMultilpeTodosFiles(unittest.TestCase):
    def test_list_dir(self):
        p = 'tests/resources/multiples/'
        paths = set(tf._list_files_in_dir(p))
        self.assertEqual(paths, set([p + '1.taskpaper', p + '2.taskpaper']))

    def test_project_title_from_path(self):
        self.assertEqual(
            tf._get_project_title('tests/resources/todos.taskpaper'),
            'todos:'
        )

    def test_from_dir(self):
        self.assertEqual(
            unicode(tf.from_dir('tests/resources/multiples')),
"""1:
\t- task 1
2:
\t- task 2"""
        )

    def test_source_filtering(self):
        t = tf.from_dir('tests/resources/multiples')
        self.assertEqual(
            unicode(t.filter('source = tests/resources/multiples/1.taskpaper')),
"""1:
\t- task 1"""
        )
        self.assertEqual(
            unicode(t.filter('source = tests/resources/multiples/2.taskpaper')),
"""2:
\t- task 2"""
        )


class TestSources(unittest.TestCase):
    filenames = ('0.taskpaper', '1.taskpaper', '2.taskpaper')
    root_path = 'tests/resources/temp/'
    content1 = """project 1:
\t- task 1
\t- task 2
"""
    content2 = """project 2:
\t- task 3 @done"""
    content3 = """- task 4
- task 5 @done

- task 6
"""
    contents = (content1, content2, content3)
    files = zip(filenames, contents)

    def root(self, path=''):
        return self.root_path + path

    def setUp(self):
        for filename, content in self.files:
            write(self.root(filename), content)

    def test_read_and_write(self):
        todos = tf.from_dir(self.root())
        tf.to_sources(todos)
        for filename, content in self.files:
            self.assertEqual(read(self.root(filename)), content)

    def test_read_filter_and_write(self):
        todos = tf.from_dir(self.root()).filter('not @done')
        tf.to_sources(todos)
        for filename, content in self.files:
            self.assertEqual(
                read(self.root(filename)),
                unicode(tf.from_text(content).filter('not @done'))
            )


class TestTodosArthmetics(unittest.TestCase):
    def setUp(self):
        self.t1 = tf.from_path('tests/resources/multiples/1.taskpaper')
        self.t2 = tf.from_path('tests/resources/multiples/2.taskpaper')

    def test_add_headless(self):
        self.assertEqual(
            unicode(self.t1 + self.t2),
"""- task 1
- task 2"""
        )

    def test_head_to_headless(self):
        self.t1 = self.t1.as_subtodos_of('project 1:')
        self.assertEqual(
            unicode(self.t1 + self.t2),
"""project 1:
\t- task 1
- task 2"""
        )

    def test_headless_to_head(self):
        self.t1 = self.t1.as_subtodos_of('project 1:')
        self.assertEqual(
            unicode(self.t2 + self.t1),
"""- task 2
project 1:
\t- task 1"""
        )

    def test_head_to_head(self):
        self.t1 = self.t1.as_subtodos_of('project 1:')
        self.t2 = self.t2.as_subtodos_of('project 2:')
        self.assertEqual(
            unicode(self.t1 + self.t2),
"""project 1:
\t- task 1
project 2:
\t- task 2"""
        )


class TestTodosModification(unittest.TestCase):
    def todos(self, text):
        self._todos = tf.from_text(text)
        return self

    def with_text(self, text):
        self._text = text
        return self

    def appended_to_result_of_get(self, query):
        item = self._todos.get_item(query)
        self._todos = self._todos.by_appending(self._text, to_item=item)
        return self

    def prepend_to_result_of_get(self, query):
        item = self._todos.get_item(query)
        self._todos = self._todos.by_prepending(self._text, to_item=item)
        return self

    def are(self, text):
        self.assertEqual(unicode(self._todos), text)
        return self

    def test_append(self):
        self.todos(
"""- 0
p1:
\t- 1
- 2"""
        ).with_text('- 1.1').appended_to_result_of_get('p1').are(
"""- 0
p1:
\t- 1
\t- 1.1
- 2"""
        ).with_text('- 2.1').appended_to_result_of_get('2').are(
"""- 0
p1:
\t- 1
\t- 1.1
- 2
\t- 2.1"""
        )

    def test_prepend(self):
        self.todos(
"""- 0
p1:
\t- 1
- 2"""
        ).with_text('- 1.1').prepend_to_result_of_get('p1').are(
"""- 0
p1:
\t- 1.1
\t- 1
- 2"""
        ).with_text('- 2.1').prepend_to_result_of_get('2').are(
"""- 0
p1:
\t- 1.1
\t- 1
- 2
\t- 2.1"""
        )

if __name__ == '__main__':
    unittest.main()
