from __future__ import print_function
# http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html

# https://gist.github.com/pslobo/f89cb16d4ad384c9fc9f

# -*- coding: UTF-8 -*-

# Script to interact with TaskPaper files in Pythonista. Currently this will mark tasks @done based on their parent/subtask status and also show the next tasks.

import re
import itertools

# Variable used for testing purposes. When in production this will be passed via
# file, clipboard or command line argument
arg = [
'/var/mobile/Applications/EE962478-374F-46A3-BAA9-6A276B8EB00D/Documents/grabArgs.py', 
'Project Done:\n\t- Task 01 @done\n\t\t- Subtask 1.01\n\t\tEste é um comentário malandro\n\t\t- Subtask 1.02\n\t\t\t- Subsubtask 1.01 @done\n\t\t\tEste é outro comentário malandro\n\t\t\t- Subsubtask 1.02\n\t\t\t\t- Subsubsubtask 1.01\n\t\t\t- Subsubtask 1.03\n\t\t- Subtask 1.03\n\t\t- Subtask 1.04\n\t- Task 02 @done\n\t\t- Subtask 2.01 @done\n\t\t- Subtask 2.02\n\t\t\t- Subsubtask 2.01 @done\n\t\t\t- Subsubtask 2.02\n\t\t\t\t- Subsubsubtask 2.01 @done\n\t\t\t- Subsubtask 2.03 @done\n\t\t- Subtask 2.03 @done\n\t\t- Subtask 2.04 @done\n\t- Task 03 @done\n\t\t- Subtask 3.01 @done\n\t\t- Subtask 3.02\n\t- Task 04 @done\n\t\t- Subtask 4.01 @done\n\t\t- Subtask 4.02 @done\n\t- Task 05 @done\n\t\t- Subtask 5.01 @done\n\t\t- Subtask 5.02 @done\n\t\t\t- Subsubtask 5.03 @done\n\t\t- Subtask 5.03 @done\n\t- Task 06 @done\n\t\t- Subtask 6.01\n\t\t\t- Subsubtask 6.01 @done\n\t\t\t- Subsubtask 6.02 @done\n\t\t- Subtask 6.02 @done\n\t- Task 07 @done\n\t\t- Subtask 7.01\n\t\t\t- Subsubtask 7.01 @done\n\t\t- Subtask 7.02\n\t\t\t- Subsubtask 7.02 @done\n\t- Task 08 @done\n\t\t- Subtask 8.01\n\t\t\t- Subsubtask 8.01 @done\n\t\t\t- Subsubtask 8.02\n\t\t\t\t- Subsubsubtask 8.01 @done\n\t\t\t\t- Subsubsubtask 8.02\n\t\t\t\t\t- Subsubsubsubtask 8.01 @done\n\t\t\t\t- Subsubsubtask 8.03 @done\n\t\t\t- Subsubtask 8.03 @done\n\t\t- Subtask 8.02 @done\n\t\t- Subtask 8.03\n\t\t\t- Subsubtask 8.04 @done\n\t\t\t- Subsubtask 8.05\n\t\t\t\t- Subsubsubtask 8.04\n\t\t\t\t\t- Subsubsubsubtask 8.02 @done\n\t\t\t- Subsubtask 8.06 @done\n\t- Task 09 @done\n\tThis is a comment\n\t\t- Subtask 9.01 @done\n\t\tThis is a subtask comment\n\t\t- Subtask 9.02\n\t\tAnother comment\n\t\t\t- Subsubtask 9.01 @done\n\t\t\t- Subsubtask 9.02 @done\n\t\t\tWhy so many comments?\n\t\t\t- Subsubtask 9.03\n\t\t\t\t- Subsubsubtask 9.01 @done\n\t\t\t\tJust another comment to break your code\n\t\t\t\t- Subsubsubtask 9.02\n\t\t\t\tBreak, break, break\n\t\t\t\t\t- Subsubsubsubtask 9.01 @done\n\t\t\t\t\tThis is the last comment, I promise\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI lied.\n\t\t\t- Subsubtask 9.04\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI love lying\n\t\t\t- Subsubtask 9.05 @done\n\t\t- Subtask 9.03 @done\n\t\tOk, this is truly the last comment.\n\t\tNah.',
'Project Done:\nThis is a project comment\n\t- Task 09\n\tThis is a comment\n\t\t- Subtask 9.01 @done\n\t\tThis is a subtask comment\n\t\t- Subtask 9.02\n\t\tAnother comment\n\t\t\t- Subsubtask 9.01 @done\n\t\t\t- Subsubtask 9.02 @done\n\t\t\tWhy so many comments?\n\t\t\t- Subsubtask 9.03\n\t\t\t\t- Subsubsubtask 9.01 @done\n\t\t\t\tJust another comment to break your code\n\t\t\t\t- Subsubsubtask 9.02\n\t\t\t\tBreak, break, break\n\t\t\t\t\t- Subsubsubsubtask 9.01 @done\n\t\t\t\t\tThis is the last comment, I promise\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI lied.\n\t\t\t- Subsubtask 9.04\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI love lying\n\t\t\t- Subsubtask 9.05 @done\n\t\t- Subtask 9.03 @done\n\t\tOk, this is truly the last comment.\n\t\tNah.',
'Inbox:\n\nProject 01:\n\t- Task 1.01\n\t\t- Subtask 01\n\t\t- Subtask 02\n\t\t- Subtask 03\n\t- Task 02 @done\n\t- Task 03\n\n/Project 02:\n\t- Task 01\n\tComentário que destruirá seu domingo\n\t\t- Primeira subtarefa\n\t\t- Segunda subtarefa\n\t\t- Terceira subtarefa @done\n\t\t- Quarta subtarefa\n\t\t\t- Primeira subsubtarefa\n\t\t\t- Segunda subsubtarefa @done\n\t\t- Quinta tarefa\n\t- Task 02\n\t- Task 03 @done\n\t- Task 04\n\nProject 03:\nSou um comentário extremamente complexo que quebrarei o seu script.\n\t- Task 01\n\t\t- Subtask 01 @done\n\t\t- Subtask 02\n\t- Task 02\n\t- Task 03\n\nProject 04:\n\t- Task 01\n\t\t- Subtask 01\n\t\t- Subtask 02 @done\n\t\t- Subtask 03\n\t\t\t- Subsubtask 01 @done\n\t\t\t- Subsubtask 02 @done\n\t\t- Subtask 04\n\t- Task 02\n\t- Task 03\n\nProject 05:\n\t- Task 01 @done\n\t- Task 02 @done\n\t- Task 03 @done\n\t- Task 04 @done\n\t\t- Subtask 01 @done\n\t\t- Subtask 02 @done\n\t\t- Subtask 03 @done\n\t- Task 05\n\nProject 06:\n\t- Task 01 @done\n\t- Task 02\n\t\t- Subtask 01\n\t\tSou outro comentário maroto que arruinará o seu dia.\n\t\t- Subtask 02\n\t\tSou a primeira linha de um comentário maldoso.\n\t\tEsta é a segunda linha do comentário acima que te fará chorar.\n\t\t- Subtask 03\n\t- Task 03\n\nProject 7:\n\t- Lavar roupa @done\n\tSou a primeira linha de um comentário maldoso.\n\t\t- Cuecas @done\n\t\t- Meias @done\n\t- Cozinhar risoto @done\n\t\t- Lavar panela @done\n\t\t- Comprar arroz @done\n\t\t- Preparar caldo @done\n\nProject 08:\n\t- Task 01\n\tSou a primeira linha de um comentário maldoso.\n\nProject 09:\n\t- Task 01']


def DoneParent2Child(l):
    """Function responsible for propagating @done tags to all subtasks.It 
    iterates over every tasks, if the task is tagged @done and has subtasks, 
    then every subtask is also tagged @done"""

    for task in l:
        if task is not l[-1] and re.search('\t+-\s.*@done.*', task):
            next_task = l[l.index(task)+1]
            if next_task.count('\t') > task.count('\t'):
                subtasks = list(itertools.takewhile(lambda x:x.count('\t') > task.count('\t'), l[l.index(next_task):]))
                for subtask in subtasks:
                    if re.search('(?!.*@done)\t+-\s.*', subtask):
                        l[l.index(subtask)]+=' @done'
    return l
    

def DoneChild2Parent(l):
    """Function responsible for propagating @done tags to every task when it's
    subtasks are all tagged @done. It iterates over every task, checks if it 
    has subtasks  and if all are @done, tags the task @done too."""

    tasks = iter([(x,y) for x,y in enumerate(l) if re.search('\t+-\s.*',y)])
    
    for k in tasks:
        if re.search('(?!.*@done)\t*-\s.*', k[1]):
            try:
                nt = tasks.next()
            except StopIteration:
                break
            if nt[1].count('\t') > k[1].count('\t'):
                subtasks = [subtask for subtask in l[k[0]:] if subtask.count('\t') > k[1].count('\t') and re.search('\t+-\s.*',subtask) ]
                if all('@done' in subtask for subtask in subtasks):
                    l[k[0]]+=' @done'
                    DoneChild2Parent(l)
                    break    
    return l
    

allTasks = arg[3].split('\n\n')
projects = [filter(None,proj.split('\n')) for proj in allTasks]

for proj in projects:
    
    tp = DoneChild2Parent(DoneParent2Child(proj))
    
    if len(tp)>0:
        tempstr = "\n".join(tp)
        if tp[0].startswith("/"):
            project = re.compile("(^[\\w/].*:*(\\n\\w.*)*)", re.M) # Find Project Name and Project Comments
            tasks = re.compile("^[^/][\\t\\w]*-??\\s??(?!.*@done).+\\n*", re.M) # Finds every line not containing @done
            print(project.match(tempstr).group()) # Prints the Project name and comment
            print("".join(tasks.findall(tempstr))) # Findall creates a list, so we print it with a join
            
        else:
            project = re.compile("(^[\\w/].*:*(\\n\\w.*)*)", re.M)
            ttasks = re.compile("(?!.*@done)(\\t-\\s.*(\\n\\t{2,}-\\s.+)*(\\n\\t+\\w.+(\\n\\t{2,}-\\s.+)*)*)", re.M) # Main match. Will eliminate tasks with @done
            tasks = re.compile("[\\t]+-??\\s??(?!.*@done).+\\n*", re.M) # Second match, will eliminate sub(sub)tasks with @done
            if ttasks.search(tempstr) is not None:
                print(project.match(tempstr).group())
                print("".join(tasks.findall(ttasks.search(tempstr).group())))