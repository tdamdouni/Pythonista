# coding: utf-8

# https://github.com/hiten2/Arachnid

# A directory search tool

import operator
import os
import time

import tkMessageBox
from Tkinter import *


def main():
    """Main method. Bound to pressing 'go' button."""
    output["text"] = ""  # CLEAR output
    if keyNpt.get():
        results = processResults(searchTree(
            dirNpt.get(), parseStrList(keyNpt.get())
        ))

        if results:
            output["text"] = "[ Search complete. ]"
            # UPDATE OUTPUT WITH SEARCH RESULTS
            tkMessageBox.showinfo("Results", results)
        else:
            output["text"] = "[ No matches found. ]"  # IF AN ERROR OCCURRED
    else:
        output["text"] = "Please fill out all fields."
    return


def parseStrList(string):
    """PARSE string INPUT TO keys"""
    return [s.strip() for s in string.split(",")]


def processResults(queries):
    """SORT AND TABULATE queries"""
    data = ""
    queries = sorted(queries.items(), key=operator.itemgetter(1))
    results = ""

    for n in range(1, len(queries) + 1):
        # SHOW MATCHES FIRST
        results += "\n[ %s : %s ]" % (queries[-n][1], queries[-n][0])
    return results


def searchFile(path, keys):
    """return matches FOUND IN FILE AT path"""
    matches = 0
    # QUIT IF FILE AT path IS UNREADABLE
    if not (lambda path: os.access(path, os.R_OK))(path):
        return matches
    with open(path, "r") as f:
        data = ''.join(f.readlines())
    for k in keys:
        while data.find(k) > -1:
            # UPDATE VALUES
            data, matches = data[data.find(k) + 1:], matches + 1
    return matches


def searchTree(dirPath, keys):
    """return queries"""
    queries = {}
    dirPath = dirPath or "./"  # SETS DEFAULT dirPath VALUE
    for root, directories, filenames in os.walk(dirPath):
        for f in filenames:
            if f == "Arachnid.py":
                continue
            path = os.path.join(root, f)
            matches = searchFile(path, keys)
            if matches > 0:
                queries[str(path)] = matches  # ONLY SHOW PATHS WITH HITS
    return queries

if __name__ == "__main__":
    # WINDOW
    window = Tk()
    window.wm_title("Arachnid")

    # FRAMES
    top = Frame(window)
    space1 = Frame(window, height=4)
    mid = Frame(window)
    space2 = Frame(window, height=4)
    bottom = Frame(window)

    # WIDGETS
    keyLbl = Label(top, text="Keywords (separate w/ commas): ")
    keyNpt = Entry(top, bg="white", width=20)

    dirLbl = Label(mid, text="Directory: ")
    dirNpt = Entry(mid, bg="white", width=20)
    go = Button(mid, command=main, text="Go")

    outputLbl = Label(bottom, text="Output: ")
    output = Label(bottom, text="[ Waiting for initial launch.... ]")

    # WIDGET PACKING
    keyLbl.pack(side=LEFT)
    keyNpt.pack(side=RIGHT)

    dirLbl.pack(side=LEFT)
    go.pack(side=RIGHT)
    dirNpt.pack()

    outputLbl.pack(side=LEFT)
    output.pack(side=RIGHT)

    # FRAME PACKING
    for f in (top, space1, mid, space2, bottom):
        f.pack()

    # REST
    window.mainloop()
