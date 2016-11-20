# coding: utf-8

# https://forum.omz-software.com/topic/1431/mysql-client/11

import mysqldb

db = mysqldb.connect(host= "http://my_host", user = "user", passwd="password", db="my_database", port = 3306)

cursor = db.cursor()

