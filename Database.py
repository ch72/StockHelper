from MySQLcommands import *

def initDatabase(hostname, username, password):

    db = mysqlInit(hostname, username, password)
    
    if (db == None): return None
    
    dbname = "stockdatabase"
    tablename = "stockinfo"

    createDatabase(db, dbname)
    columns = {'ticker':'char(5)', 'price':'int', 'valuation':'float(10,2)', 'projectedgrowth':'float(10,2)'}
    createTable(db, tablename, columns, dbname)

    return db
