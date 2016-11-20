# https://forum.omz-software.com/topic/3334/mysql-in-pythonista/3

# Insert

import mysqldb

db = mysqldb.connect(host= "mysql.my_domain.co.uk", user = "my_username", passwd="my_password", db="my_database", port = 3306)

c = db.cursor()

c.execute("INSERT INTO my_table (my_column1, my_column_2) VALUES (%s, %s)", (my_value_1, my_value_2))

db.commit()

db.disconnect()

# --------------------

# Select

import mysqldb

db = mysqldb.connect(host= "mysql.my_domain.co.uk", user = "my_username", passwd="my_password", db="my_database", port = 3306)

c = db.cursor()

c.execute("SELECT * FROM my_table ORDER BY my_column_1 DESC LIMIT 0, 100")

my_variable = c.fetchall()

db.disconnect()

# --------------------

