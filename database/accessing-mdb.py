import pyodbc
ODBC_DRIVER = '{Microsoft Access Driver (*.mdb)}'

connstr = 'DRIVER={0};DBQ={1}'.format(ODBC_DRIVER, 'Scidb.mdb')
conn = pyodbc.connect(connstr)

cur = conn.cursor()
cur.execute('SELECT * FROM table')

