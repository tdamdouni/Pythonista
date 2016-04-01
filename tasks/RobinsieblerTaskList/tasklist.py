#------------------------------------------
# Name:     tasklist
# Purpose:  Class for the creation/management of tasks
#
# Author:   Robin Siebler
# Created:  7/14/13
#------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/14/13'

import datetime

# TODO: add option to sort by date

class Task:
    last_id = 0

    def __init__(self, note, priority, tags=''):
        """Initialize a Task object.

        :param note: a string containing the task
        :param priority: the priority of the task (low, medium, high)
        :param tags: any desired tags for the task
        """

        self.note = note
        self.priority = priority
        self.tags = tags
        self.creation_date = datetime.date.today().strftime("%m/%d/%Y")
        Task.last_id += 1
        self.id = Task.last_id

    def __str__(self):
        fmt = '{}: {}\n\tPriority: {}\n\tTags: {}'
        return fmt.format(self.id, self.note, self.priority, self.tags)

    def match(self, search_string):
        """Return a list of tasks where search_string is found in either the notes or tags.

        :return: a list of matches
        """

        return search_string in self.note.lower() or search_string in self.tags.lower()

class TaskList:
    def __init__(self):
        self.tasks = []

    def __str__(self):
        return '\n'.join([str(task) for task in self.tasks])

    def add_task(self, note, priority, tags):
        """Add a new task to the task list.

        :param note: a string containing the task
        :param priority: the priority of the task (low, medium, high)
        :param tags: any desired tags for the task
        """

        self.tasks.append(Task(note, priority, tags))

    def delete_task(self, task_id):
        """Delete the given task.

        :param task_id: id of the task to delete
        """

        task = self._find_task(task_id)
        if task:
            self.tasks.remove(task)

    def search(self, search_string):
        """Return all task that match the given search string

        :param search_string: search string
        :return: task list
        """

        return [task for task in self.tasks if task.match(search_string)]

    def _find_task(self, task_id):
        """Find a task by task.id

        :param task_id: The task.id for the task to find.
        :return: a task object if found, otherwise None
        """

        for task in self.tasks:
            if str(task.id) == str(task_id):
                return task
        return None

    def _renumber_tasks(self):
        """Renumber all of the tasks. Useful when a task is deleted."""

        Task.last_id = 0
        for task in self.tasks:
            Task.last_id += 1
            task.id = Task.last_id

if __name__ == '__main__':
    from menu import Menu
    Menu().run()  # replace with a call to unit tests?
