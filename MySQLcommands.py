import mysql.connector

# Start up method for mySQL
# mydb provides a connector to database
def mysqlInit(hostname, username, passwrd):

  # Connects to MySQL database
  try: 
    mydb = mysql.connector.connect(
      host=hostname,
      user=username,
      password=passwrd
    )
  except: return None

  return mydb

# Creates a database on connector (dbinstance)
def createDatabase(dbinstance, dbname):

  line = dbinstance.cursor()

  # Creates a database if it does not exist
  try: line.execute(f"CREATE DATABASE {dbname}")
  except: pass #print("createDatabase: Database already exists")

# Creates a table in a database on connector
def createTable(dbinstance, tablename, columnsForTable, dbname = None):

  line = dbinstance.cursor()

  command = "CREATE TABLE " + tablename + "("
  for columns, types in columnsForTable.items():
    command += columns + " " + types + ", "
  command = command[0:-2] + ")"

  if (dbname != None): line.execute(f"USE {dbname}")

  # Creates a table if it does not exist
  try: line.execute(command)
  except: pass #print("createTable: Table already exists")

# Deletes a database on connector
def deleteDatabase(dbinstance, dbname):

  line = dbinstance.cursor()

  try: line.execute(f"DROP DATABASE {dbname}")
  except: print("deleteDatabase: Database for deletion does not exist")

# Deletes a table in a database on connector
def deleteTable(dbinstance, tablename, dbname = None):

  line = dbinstance.cursor()

  if (dbname != None): line.execute(f"USE {dbname}")

  try: line.execute(f"DROP TABLE {tablename}")
  except: print("deleteTable: Table for deletion does not exist")

# Searches table for desired value(s)
def searchTable(dbinstance, tablename, condition = None, orderBy = None, columnsToShow = None, dbname = None):

  line = dbinstance.cursor()

  command = "SELECT "

  if (columnsToShow != None):
    for column in columnsToShow:
      command += str(column) + ", "
    command = command[0:-2]
  else: command += "*"

  command += " FROM " + tablename

  # Currently, functional only supports one condition (TODO: Allow for more)
  if (condition != None): command += " WHERE " + condition 

  if (orderBy != None): command += " ORDER BY " + orderBy
  
  if (dbname != None): line.execute(f"USE {dbname}")

  try: 
    line.execute(command)
    return (line.fetchall())
  except: 
    print("searchTable: Error")
    return None

# Displays table in its entirity 
def showTable(dbinstance, tablename, columnsToShow = None, orderBy = None, dbname = None):

  line = dbinstance.cursor()
  table = searchTable(dbinstance, tablename, None, orderBy, columnsToShow, dbname)
  if table == None: 
    print ("showTable: Failed to find table to view")
    return None
  for entry in table:
    print(entry)

# Adds a row to the specified table
# If condition contains string, make sure to use ''
def insertRow(dbinstance, tablename, columnValues, dbname = None):

  line = dbinstance.cursor()

  if (dbname != None): line.execute(f"USE {dbname}")

  command = "INSERT INTO " + tablename + " VALUES("
  for column in columnValues: 
    if (isinstance(column, str)): command += '\'' + column + '\'' + ", "
    else: command += str(column) + ", "
  command = command[0:-2] + ")"

  try: 
    line.execute(command)
    dbinstance.commit()
  except: print("insertRow: Inputted table does not exist or values are invalid")

# Deletes a row from the specified table
# If condition contains string, make sure to use ''
def deleteRow(dbinstance, tablename, condition = None, dbname = None):

  line = dbinstance.cursor()

  if (dbname != None): line.execute(f"USE {dbname}")

  try: 
    line.execute(f"DELETE FROM {tablename} WHERE {condition}")
    dbinstance.commit()
  except: print ("deleteRow: Inputted table does not exist or condition is invalid")