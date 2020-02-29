#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script walks a given directory and creates a pdf for every .md or .markup file it finds
# The PDF is recreated only when changes to the markup file is detected
# Hashsums are kept in a sqlite database (fileHashes.db)
# Script uses pandoc for markdown to pdf transformation

from __future__ import print_function
import os, sqlite3, modsqlite

directory = "/path/to/markdown/files"
template = "template.tex"

# ---------- put/get specific for the hasher app ----------

# add or update
def put(c, conn, tableName, file, shasum):
    oldShasum = modsqlite.readFrom(c, conn, tableName, "shasum", "file", file)
    if (oldShasum == None):
        # we need to add the value!
        # returns True when added -> also update the pdf!
        return modsqlite.insertInto(c, conn, tableName, "'{}', '{}'".format(file, shasum))
    else:
        # we need to test if the oldValue is the same as the new value
        if (oldShasum == shasum):
            # return False -> no need to update the pdf!
            return False
        else:
            # returns True when updated -> also update the pdf!
            return modsqlite.update(c, conn, tableName, "shasum", shasum, "file", file)

# just a simple wrapper for readFrom to match the put/get syntax
def get(c, conn, tableName, value, condL, condR):
    return modsqlite.readFrom(c, conn, tableName, value, condL, condR)

# ---------- hashing ----------

# calls shasum via popen; maybe faster solution possible
def shasum(file):
    try:
        inStream = os.popen("shasum " + file)
        input = inStream.readline()
        return input[0:40]
    except:
        return 0

# ---------- program flow ----------

# prepare db & connection
conn = sqlite3.connect('fileHashes.db')
c = conn.cursor()
modsqlite.createTable(c, conn, "hashes", "file text, shasum text")

# walk through the given folder
for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if((".md" in filename) or (".markdown" in filename)) and (".pdf" not in filename):
            file = os.path.join(dirname, filename)
            sha = shasum(file)
            print(file)
            if put(c, conn, "hashes", file, sha):
                print("Updating...")
                cmd = "pandoc {} -f markdown --template {} --toc -s -o {}.pdf".format(file, template, file)
                os.popen(cmd)
            else:
                print("Skipping...")

conn.close
