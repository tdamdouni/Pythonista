# https://forum.omz-software.com/topic/1431/mysql-client/17

try:
	import pymysql as mysqldb
except ImportError:
	import mysqldb
	
def dbConnect():
	#port 3306 is the default for mysql
	#returns false if it can't successfully connect
	username = "username"
	password = "password"
	dataBase = "databaseOnServer"
	porty = 3306
	try:
		conn = mysqldb.connect(host="host.something.com", user=username,passwd=password,db = dataBase,port=porty)
	except mysqldb.err.OperationalError:
		print("Can't connect. Check your hostname/user/password info.")
		conn = False
		
	return conn
	
	
def getLatestSavedEntry(tableName):
	#gets the latest entry, the one with largest ID (must be a table with "ID set as an auto-incrementing primary key")
	#createTable function does this.
	conn=dbConnect()
	if conn ==False:
		print("no connection")
		return
		
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT * FROM "+str(tableName)+" where ID = (SELECT MAX(ID) FROM "+tableName+")")
		lastEntryData=cursor.fetchone()
		if lastEntryData == None:
			lastEntryData = ["doesnt","exist...nope"]
	except:
		lastEntryData =["table","doesn't","exist","...probably"]
		print(lastEntryData)
		
	cursor.close()
	return lastEntryData
	
	
def createTable(tableName):
	conn = dbConnect()
	if conn ==False:
		print("no connection")
		return
		
	cursor=conn.cursor()
	#adjust this string with the sequel commands you'd like, columns etc.
	sequelString = "CREATE TABLE "+str(tableName)+"(ID INT(11) PRIMARY KEY AUTO_INCREMENT, uuid VARCHAR(50),request_at DOUBLE, duration INT, totalDuration INT, ratingHistoryCalculatedAverage DOUBLE,ratingHistory5 INT, ratingHistory4 INT, ratingHistory3 INT, ratingHistory2 INT, ratingHistory1 INT, Surge VARCHAR(30), fare DOUBLE, fareTakeHome DOUBLE, Distance DOUBLE)"
	
	
	try:
		print(".....trying table creation")
		cursor.execute(sequelString)
		print("created new table!")
		return "Success"
	except:
		print("table couldnt be created...")
		return "Failure to create"
		
	cursor.close()
	
	
	
def getSequelData(tableName):
	#this gets all of the data in your selected database and table, returns False if
	conn=dbConnect()
	if conn ==False:
		print("no connection")
		return
		
	cursor = conn.cursor ()
	
	#get the vertsion of your mysql
	cursor.execute("SELECT VERSION()")
	row = cursor.fetchone()
	
	queryString = "SELECT * FROM "+str(tableName)
	try:
		cursor.execute(queryString)
		data=cursor.fetchall()
		print(data)
		
	except mysqldb.err.ProgrammingError:
		print("DOESN'T EXIST, YOU MUST CREATE THIS TABLE TO BE ABLE TO FETCH ITS CONTENTS.")
		data = False
		
		
		
	cursor.close()
	
	return data
	
def doesTableExist(tableNameToCheck):
	tableNameToCheck = str(tableNameToCheck)
	tableList = getTableList()
	if tableList ==False:
		print("no connection")
		return
		
	for table in tableList:
		#tableList is a list of tuples of unicode w/second of tuple empty
		existingTable = str(table[0])#gets to unicode string
		#print(existingTable,"???",tableNameToCheck)
		if existingTable == tableNameToCheck:
			print("table "+tableNameToCheck+" already exists. Yay!")
			userTableExists = True
			break
		else:
			userTableExists = False
			
	if userTableExists:
		#print("Table exists. moving on.")
		return True
	elif not userTableExists:
		#print("Table not found. Maybe you should create it.")
		return False
		
def getTableList():
	conn = dbConnect()
	if conn ==False:
		print("no connection")
		return False
		
	cursor = conn.cursor()
	#cursor.execute("select * from information_schema.tables")
	cursor.execute("SHOW TABLES")
	tableList=cursor.fetchall()
	#print(tableList)
	cursor.close()
	
	return tableList
	
	
	
if __name__=="__main__":

	#tests
	
	print( getLatestSavedEntry("someTable") )
	print( createTable("someTable") )
	print( getSequelData("someTable") )
	print( getTableList() )
	print( "table exists?:",doesTableExist("someTable") )

