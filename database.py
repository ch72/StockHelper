import mysql.connector

# Start up method for mySQL
# mydb provides a connector to database
def mysql_init(hostname, username, passwrd):

  # Connects to MySQL database
  mydb = mysql.connector.connect(
    host=hostname,
    user=username,
    password=passwrd
  )

  return mydb

# Creates a database on connector (dbinstance)
def createDatabase(dbname, dbinstance):

  line = dbinstance.cursor()

  # Creates a database if it does not exist
  try: line.execute(f"CREATE DATABASE {dbname}")
  except: print("Database already exists")

# Creates a table in a database on connector
def createTable(tablename, dbinstance, columnDict, dbname = None):

  line = dbinstance.cursor()

  cols = "CREATE TABLE " + tablename + "("
  for columns, types in columnDict.items():
    cols += columns + " " + types + ", "
  cols = cols[0:len(cols)-2] + ")"

  if (dbname != None): line.execute(f"USE {dbname}")

  # Creates a table if it does not exist
  try: line.execute(cols)
  except: print("Table already exists")

# Deletes a database on connector
def deleteDatabase(dbinstance, dbname):

  line = dbinstance.cursor()

  try: line.execute(f"DROP DATABASE {dbname}")
  except: print("Database for deletion does not exist")

# Deletes a table in a database on connector
def deleteTable(tablename, dbinstance, dbname = None):

  line = dbinstance.cursor()

  if (dbname == None): line.execute(f"USE {dbname}")

  try: line.execute(f"DROP TABLE {tablename}")
  except: print("Table for deletion does not exist")

#TODO: Finish by adding columns
# Adds a row to the specified table
def insertRow(tablename, dbinstance, columns, dbname = None):

  line = dbinstance.cursor()

  if (dbname == None): line.execute(f"USE {dbname}")

  try: line.execute(f"ALTER TABLE {tablename} ADD ")
  except: print("Inputted table does not exist")
