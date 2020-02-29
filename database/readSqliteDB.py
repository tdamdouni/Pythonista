from __future__ import print_function
# http://omz-forums.appspot.com/pythonista/post/5531591459733504
# coding: utf-8
import sqlite3
 
conn = sqlite3.connect("mydatabase.db")
 
cursor = conn.cursor()

conn.execute("""DROP TABLE IF EXISTS alicelist""")
cursor.execute("""CREATE TABLE alicelist
                  (name text, character text, scenes text) 
               """)

alicelist = [('Kate Threlfall', 'Alice', '10'),
          ('Ailsa', 'Mother/White Queen', '5'),
          ('Chloe Harley', 'Sister/Red Queen','5'),
          ('Olivia Pewsey', 'Tweedle Dum', '4'),
          ('Anna Winstanley', 'Tweedle Dee', '4')]
cursor.executemany("INSERT INTO alicelist VALUES (?,?,?)", alicelist)
conn.commit()

print("\nHere's a listing of all the records in the table:\n")
for row in cursor.execute("SELECT rowid, * FROM alicelist ORDER BY character"):
	print(row)
print(cursor.fetchall())