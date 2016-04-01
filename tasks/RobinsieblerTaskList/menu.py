# ------------------------------------------
# Name:     menu
# Purpose:  Menu interface (with GUI) for creating/managing tasks.
#
# Author:   Robin Siebler
# Created:  7/28/14
#------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/28/14'

import speech, sys, ui
import help, util
import tasklist; reload(tasklist)


class Menu:

    def __init__(self):
        """Initialize the task list."""

        self.tasklist = tasklist.TaskList()
        self.current_task = ''
        self.current_task_file = ''
        self.main_view = ''
        self.controls_enabled = False

    def display_message(self, message):
        """Display any warnings or errors to the user."""

        self.message_dialog = ui.load_view('dialogs/message')
        self.message_dialog['label1'].text = message
        self.message_dialog.present('popover', popover_location=(500, 500))

#    def say_message(self, message):
#        speech.say(message, self.language, self.speech_rate)

    def show_tasks(self, sender, tasks=None):
        """Display the tasks (in ID order)

        :param tasks: tasks object
        """

        if not tasks:
            tasks = self.tasklist.tasks
        tv_text = ""
        if tasks:
            if not self.controls_enabled:
                #enable controls if there are tasks loaded
                buttons = 'number priority save delete_task modify search speak'
                for button in buttons.split():
                    # turn on invalid controls
                    self.main_view['button_' + button].enabled = True
                self.controls_enabled = True
            for task in tasks:
                tv_text += '{}: {}\n\tPriority: {}\n\tTags: {}\n'.format(task.id, task.note, task.priority, task.tags)
        else:
            tv_text = '\nThere are no tasks to display!\n'

        self.task_textview.text = tv_text

    def show_tasks_by_priority(self, sender, tasks=None):

        """Display the tasks (in Priority order)

        :param tasks: tasks object
        """

        def task_as_str(task):

            return '{}: {}\n\tTags: {}'.format(task.id, task.note, task.tags)

        def priority_text(priority, tasks):

            text = '{}:\n{}\n'.format(priority, '-' * 20)
            new_tasks = [task_as_str(t) for t in tasks
                             if t.priority == priority]
            text += '\n'.join(new_tasks) or 'There are no tasks to display!'
            return text

        if not tasks:
            tasks = self.tasklist.tasks

        self.task_textview.text = '\n\n'.join(priority_text(p, tasks)
                                              for p in 'High Medium Low'.split())

    def prompt_search(self, sender):
        """Prompt the user for a search string."""

        if self.main_view['button_search'].title == 'Show All':
            self.main_view['button_search'].title = 'Search'
            self.show_tasks(None)
        else:
            self.search_dialog = ui.load_view('dialogs/search_tasks')
            self.search_dialog['txt_search'].begin_editing()
            self.search_dialog['txt_search'].delegate = self
            self.search_dialog.present('popover', popover_location=(500, 500))

    def search_tasks(self, sender):
        """Search the task list for a task whose note or tag contains the user provided search string."""

        search_string = self.search_dialog['txt_search'].text.lower()
        if search_string:
            tasks = self.tasklist.search(search_string)
            if tasks:
                self.search_dialog.close()
                self.main_view['button_search'].title = 'Show All'
                self.show_tasks(None, tasks=tasks)
            else:
                message = 'There were no tasks containing "{}".'.format(search_string)
                self.display_message(message)

    def prompt_add(self, sender):
        """Prompt the user to add a task."""

        self.add_dialog = ui.load_view('dialogs/add_task')
        self.add_dialog['button_save'].enabled = False
        self.add_dialog['txt_add_task'].delegate = self
        self.add_dialog['txt_add_task'].begin_editing()
        self.add_dialog.present('popover', popover_location=(500, 500))

    def add_task(self, sender):
        """Add a new task."""

        note = self.add_dialog['txt_add_task'].text
        priority_num = self.add_dialog['segmentedcontrol1'].selected_index
        priority = 'Low Medium High'.split()[priority_num]
        tags = self.add_dialog['txt_add_tags'].text
        self.tasklist.add_task(note, priority, tags)
        self.add_dialog.close()
        self.show_tasks(None)

    def prompt_delete_file(self, sender):
        """Prompt the user to delete a task file."""

        self.delete_dialog = ui.load_view('dialogs/delete_task_file')
        self.delete_dialog['txt_filename'].begin_editing()
        self.delete_dialog.present('popover', popover_location=(500, 500))

    def delete_file(self, sender):
        """Delete a task file."""

        task_file = self.delete_dialog['txt_filename'].text
        if not task_file == '':
            task_file = util.validate_file(task_file)
        if task_file:
            self.delete_dialog.close()
            util.delete(task_file)
        else:
            self.display_message(self.delete_dialog['txt_filename'].text + ' is not a valid file!')
            self.delete_dialog['txt_filename'].text = ''

    def prompt_delete_task(self, sender):
        """Prompt the user to delete a task."""

        self.delete_dialog = ui.load_view('dialogs/delete_task')
        self.delete_dialog['txt_del_task'].begin_editing()
        self.delete_dialog['txt_del_task'].delegate = self
        self.delete_dialog.present('popover', popover_location=(500, 500))

    def delete_task(self, sender):
        """Delete a task."""

        task_id = self.delete_dialog['txt_del_task'].text
        if task_id:
            task_id = self._validate_task_id(task_id)
            if task_id:
                self.delete_dialog.close()
                self.tasklist.delete_task(task_id)
                self.tasklist._renumber_tasks()
                self.show_tasks(None)
            else:
                self.delete_dialog['txt_del_task'].text = ''

    def prompt_modify_task_number(self, sender):
        """Prompt the user for the number of the task to modify."""

        self.modify_dialog = ui.load_view('dialogs/modify_task_number')
        self.modify_dialog['txt_mod_task_num'].begin_editing()
        self.modify_dialog['txt_mod_task_num'].delegate = self
        self.modify_dialog.present('popover', popover_location=(500, 500))

    def modify_task(self, sender):
        """Change the fields of a task."""

        task_id = self._validate_task_id(self.modify_dialog['txt_mod_task_num'].text)
        if task_id:
            self.current_task = self.tasklist._find_task(task_id)
            self.modify_dialog.close()
            self.modify_dialog = ui.load_view('dialogs/modify_task')
            self.modify_dialog['txt_mod_task'].delegate = self
            self.modify_dialog['txt_mod_task'].text = self.current_task.note
            self.modify_dialog['segmentedcontrol1'].selected_index = ['Low', 'Medium', 'High'].index(self.current_task.priority)
            self.modify_dialog['txt_mod_tags'].text = self.current_task.tags
            self.modify_dialog.present('popover', popover_location=(500, 500))

    def save_modified_task(self, sender):
        """Save the contents of the modified task."""

        self.current_task.note = self.modify_dialog['txt_mod_task'].text
        priority_num = self.modify_dialog['segmentedcontrol1'].selected_index
        self.current_task.priority = 'Low Medium High'.split()[priority_num]
        self.current_task.tags = self.modify_dialog['txt_mod_tags'].text
        self.modify_dialog.close()
        self.show_tasks(None)

    def prompt_load(self, sender):
        """Prompt the user for the name of a task file."""

        self.load_dialog = ui.load_view('dialogs/load_task_file')
        self.load_dialog['txt_load'].begin_editing()
        self.load_dialog['txt_load'].delegate = self
        self.load_dialog.present('popover', popover_location=(500, 500))

    def load_tasks(self, sender):
        """Retrieve the contents of the task file."""

        task_file = self.load_dialog['txt_load'].text
        if task_file:
            task_file = util.validate_file(task_file)
            if task_file:
                self.load_dialog.close()
                self.tasklist.tasks = util.load(task_file)
                self.current_task_file = task_file
                tasklist.Task.last_id = len(self.tasklist.tasks)
                self.show_tasks(None)
            else:
                self.display_message(self.load_dialog['txt_load'].text + ' is not a valid file')
                self.load_dialog['txt_load'].text = ''

    def prompt_save(self, sender):
        """Prompt the user for the name of a task file."""

        self.save_dialog = ui.load_view('dialogs/save_task_file')
        self.save_dialog['txt_save_file'].begin_editing()
        self.save_dialog['txt_save_file'].delegate = self
        self.save_dialog.present('popover', popover_location=(500, 500))

    def save_tasks(self, sender):
        """Save the tasks to the specified file."""

        task_file = self.save_dialog['txt_save_file'].text
        if task_file:
            if task_file.rfind('.tsk', len(task_file) - 4) == -1:
                task_file += '.tsk'
            self.save_dialog.close()
            if task_file == self.current_task_file:
                # some bug; even though the file should be closed, I can't overwrite it
                util.delete(task_file)
            util.save(self.tasklist.tasks, task_file)
        else:
            self.save_dialog['txt_save_file'].text = ''

    def prompt_speak(self, sender):
        """Prompt the user for the task(s) to speak."""

        self.speech_rate = 0.3
        self.language = 'en-GB'
        self.prompt_dialog = ui.load_view('dialogs/speak_task_number')
        self.prompt_dialog['button_select'].enabled = False
        self.prompt_dialog['txt_speak_number'].delegate = self
        self.prompt_dialog["segmentedcontrol1"].action = self.display_speak_options
        self.prompt_dialog['txt_speak_number'].begin_editing()
        self.prompt_dialog.present('popover', popover_location=(500, 500))

    def display_speak_options(self, sender):
        """Display the controls to enter a number"""

        # if 'recite a task' is selected, reveal  the appropriate controls
        if self.prompt_dialog['segmentedcontrol1'].selected_index == 0:
            self.prompt_dialog['label1'].hidden = False
            self.prompt_dialog['txt_speak_number'].hidden = False
            # if no task number is provided, disable the button
            if self.prompt_dialog['txt_speak_number'].text == '':
                self.prompt_dialog['button_select'].enabled = False
            else:
                self.prompt_dialog['button_select'].enabled = True
        else:
            # otherwise, hide them
            self.prompt_dialog['label1'].hidden = True
            self.prompt_dialog['txt_speak_number'].hidden = True
            self.prompt_dialog['button_select'].enabled = True

    def enable_select(self, sender):
        """Enable the Select button after a task # has been provided."""

        self.prompt_dialog['button_select'].enabled = True
        self.main_view.set_needs_display()

    def process_speak_request(self, sender):
        """Determine which task(s) to recite"""

        recite = self.prompt_dialog['segmentedcontrol1'].selected_index
        if recite == 0:
            task_id = self._validate_task_id(self.prompt_dialog['txt_speak_number'].text)
            if task_id:
                self.prompt_dialog.close()
                self.current_task = self.tasklist._find_task(task_id)
                self.speak_task(self.current_task)
            else:
                self.prompt_dialog['txt_speak_number'].text = ''
                self.prompt_dialog['button_select'].enabled = False
        else:
            self.prompt_dialog.close()
            for task in self.tasklist.tasks:
                self.speak_task(task)
        speech.say('Recitation complete.', self.language, self.speech_rate)

    def speak_task(self, task):
        """Recite the provided task"""

        if not task:
            return
        if task.tags:
            fmt = 'Task number {}, priority: {}, {}, This task has the following tags: {}'
            msg = fmt.format(task.id, task.priority, task.note, ' and '.join(task.tags.split()))
        else:
            fmt = 'Task number {}, priority: {}, {}, This task does not have any tags.'
            msg = fmt.format(task.id, task.priority, task.note)
        speech.say(msg, self.language, self.speech_rate)

    def _validate_task_id(self, task_id):
        """Validate the given task ID.

        :return: False if an invalid ID was provided, otherwise a string containing the valid task id.
        """
        if task_id:
            if task_id.isdecimal() and int(task_id) <= len(self.tasklist.tasks):
                return task_id
            else:
                self.display_message('{} is not an existing task!'.format(task_id))
                return None

    def prompt_language(self, sender):
        """Prompt the user to select a language and speak rate."""

        # set languages
        self.lang_list = [
            {'title': 'Arabic (Saudi Arabia)', 'code': 'ar-SA'},
            {'title': 'Czech (Czech Republic)', 'code': 'cs-CZ'},
            {'title': 'Danish (Denmark)', 'code': 'da-DK'},
            {'title': 'Dutch (Belgium)', 'code': 'nl-BE'},
            {'title': 'Dutch (Netherlands)', 'code': 'nl-NL'},
            {'title': 'English (Australian)', 'code': 'en-AU'},
            {'title': 'English (Ireland)', 'code': 'en-IE'},
            {'title': 'English (South Africa)', 'code': 'en-ZA'},
            {'title': 'English (United Kingdom)', 'code': 'en-GB'},
            {'title': 'English (United States)', 'code': 'en-US'},
            {'title': 'Finnish (Finland)', 'code': 'fi-FI'},
            {'title': 'French (Canadian)', 'code': 'fr-CA'},
            {'title': 'French', 'code': 'fr-FR'},
            {'title': 'German (Germany)', 'code': 'de-DE'},
            {'title': 'Greek (Greece)', 'code': 'el-GR'},
            {'title': 'Hindi (India)', 'code': 'hi-IN'},
            {'title': 'Hungarian (Hungary)', 'code': 'hu-HU'},
            {'title': 'Indonesian (Indonesia)', 'code': 'id-ID'},
            {'title': 'Italian (Italy)', 'code': 'it-IT'},
            {'title': 'Japanese (Japan)', 'code': 'ja-JP'},
            {'title': 'Korean (South Korea)', 'code': 'ko-KR'},
            {'title': 'Norwegian (Norway)', 'code': 'no-NO'},
            {'title': 'Polish (Poland)', 'code': 'pl-PL'},
            {'title': 'Portuguese (Brazil)', 'code': 'pt-BR'},
            {'title': 'Portuguese (Portugal)', 'code': 'pt-PT'},
            {'title': 'Romanian (Romania)', 'code': 'ro-RO'},
            {'title': 'Russian (Russia)', 'code': 'ru-RU'},
            {'title': 'Slovak (Slovakia) ', 'code': 'sk-SK'},
            {'title': 'Spanish (Mexico)', 'code': 'es-MX'},
            {'title': 'Spanish (Spain)', 'code': 'es-ES'},
            {'title': 'Swedish (Sweden)', 'code': 'sv-SE'},
            {'title': 'Thai (Thailand)', 'code': 'th-TH'},
            {'title': 'Turkish (Turkey)', 'code': 'tr-TR'},
            {'title': 'Chinese (China)', 'code': 'zh-CN'},
            {'title': 'Chinese (Hong Kong SAR China)', 'code': 'zh-HK'},
            {'title': 'Chinese (Taiwan)', 'code': 'zh-Tw'}
        ]

        self.prompt_lang = ui.load_view('dialogs/select_language')
        table = self.prompt_lang['tableview1']
        listsource = ui.ListDataSource(self.lang_list)
        table.data_source = listsource
        table.delegate = listsource
        listsource.action = self.set_language
        self.prompt_lang.present('sheet')

    def set_language(self, sender):
        """Set the language used for recitation based upon user selection."""

        self.language = self.lang_list[self.prompt_lang['tableview1'].selected_row[1]]['code']
        self.prompt_dialog['label_language'].text = self.lang_list[self.prompt_lang['tableview1'].selected_row[1]]['title']
        self.prompt_lang.close()

    def update_label(self, sender):
        """Update the speech rate label as the slider value changes."""

        self.prompt_dialog['label_rate'].text = '{:.2f}'.format(self.prompt_dialog['slider1'].value)
        self.speech_rate = float(self.prompt_dialog['label_rate'].text)

    def textfield_did_change(self, textfield):
        """Handle when a text field changes."""

        if textfield.name == 'txt_speak_number':
            view = textfield.superview
            button = view['button_select']
            button.enabled = textfield.text != ''
        elif textfield.name == 'txt_add_task':
            view = textfield.superview
            button = view['button_save']
            button.enabled = textfield.text != ''
        elif textfield.name == 'txt_mod_task':
            view = textfield.superview
            button = view['button_save']
            button.enabled = textfield.text != ''


    def textfield_should_return(self, textfield):
        """Function that should be executed when Enter is pressed."""

        if textfield.name == 'txt_speak_number':
            self.process_speak_request(None)
        elif textfield.name == 'txt_search':
            self.search_tasks(None)
        elif textfield.name == 'txt_load':
            self.load_tasks(None)
        elif textfield.name == 'txt_del_task':
            self.delete_task(None )
        elif textfield.name == 'txt_mod_task_num':
            self.modify_task(None)
        elif textfield.name == 'txt_save_file':
            self.save_tasks(None)
        return True

    def run(self):
        """Let's get the party started!"""

        self.main_view = ui.load_view('menu')
        buttons = 'number priority save delete_task modify search speak'
        for button in buttons.split():
            # turn off invalid controls
            self.main_view['button_' + button].enabled = False
        self.main_view.present('full_screen')
        self.task_textview = self.main_view['task_textview']
        self.task_textview.text = help.help_text

if __name__ == '__main__':
    Menu().run()
