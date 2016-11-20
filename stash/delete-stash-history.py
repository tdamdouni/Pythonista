# coding: utf-8

# https://forum.omz-software.com/topic/3020/deleting-stash-history

# stash probably keeps the history in memory while running, and writes it to the history file later. This means that deleting the history file from stash does not clear the history, because the copy in memory is not cleared. To clear the history you can probably run something like import os; os.remove(os.path.expanduser("~/Documents/.stash_history")) in the Python prompt (while stash is not running). I don't remember where exactly the .stash_history file is located, so you may need to adjust the path.

import os; os.remove(os.path.expanduser("~/Documents/.stash_history"))

