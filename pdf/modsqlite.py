#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------- some sqlite functions ----------

# creates a new table
def createTable(c, conn, tableName, structure):
    cmd = "CREATE TABLE {} ({})".format(tableName, structure)
    #print cmd
    try:
        c.execute(cmd)
        conn.commit()
        return True
    except:
        #print "Table {} exists".format(tableName)
        return False

# inserts values into a table
def insertInto(c, conn, tableName, value):
    cmd = "INSERT INTO {} VALUES({})".format(tableName, value)
    #print cmd
    try:
        c.execute(cmd)
        conn.commit()
        return True #worked
    except:
        #print "Problem inserting {}".format(value)
        return False #failed

# updates values where some condition matches
def update(c, conn, tableName, newL, newR, condL, condR):
    cmd = "UPDATE {} SET {}='{}' WHERE ({}='{}')".format(tableName, newL, newR, condL, condR)
    #print cmd
    try:
        c.execute(cmd)
        conn.commit()
        return True #worked
    except:
        #print "Problem updating {}".format(condL)
        return False #failed

# reads values from table where some condition matches
def readFrom(c, conn, tableName, value, condL, condR):
    cmd = "SELECT {} FROM {} WHERE ({}='{}')".format(value, tableName, condL, condR)
    #print cmd
    try:
        c.execute(cmd)
        value = c.fetchone()[0]
        return value
    except:
        #print "No entry found for {}={}".format(condL, condR)
        return None
