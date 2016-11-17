# coding: utf-8

# https://forum.omz-software.com/topic/2915/delete-photos-from-camera-roll/7

# This is only a little bit off-topic, but what does the skeleton code even do? Like the:

if __name__ == "__main__":
    # do program and functions here...

# Is this specifically for something, or is it just good practice?

# I only ask this because I see people do it everywhere, and I've never learned what it does, and if it's useful for something.

# sometimes you want to write a script that can be run directly. sometimes you want a module that can be imported.

# The if __name__==__main__ checks if tou are running the script instead of importing it.

# Sometimes you also want both. Some modules in the standard library can be imported (obviously) but are also command-line utilities. For example, you can import timeit in a script to time Python code programmatically, but you can also run python -m timeit <code to time> (in a shell) to quickly time the given line of Python code.

# I like to put all "main" code of a program inside a if __name__ == "__main__" block, so just in case I import a script by accident it doesn't start deleting photos from my library.

