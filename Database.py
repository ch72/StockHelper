from MySQLcommands import *
import math

def initDatabase(hostname, username, password):

    db = mysqlInit(hostname, username, password)
    
    if (db == None): return None
    
    dbname = "stockdatabase"
    tablename = "stockinfo"

    createDatabase(db, dbname)
    columns = {'ticker':'char(5)', 'price':'int', 'valuation':'float(10,2)', 'projectedgrowth':'float(10,2)', 'grossmargin':'float(4,2)'}
    createTable(db, tablename, columns, dbname)

    return db

# A crude estimation of the stock's value compared to its peers (higher=better)
# Does not take profitability/balance sheet, moat, optionality, leadership, etc into consideration
# so it is very limited in its effectiveness
# It's also mostly for fun, so don't take these ratings too seriously
def estimateValue(dbinstance, ticker):

    entry = searchTable(dbinstance, "stockinfo", condition=f'ticker={ticker}')[0]

    if (entry[3] < 10): 
        if (entry[2] > 1): return (int((1/entry[2])*math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100))
        else: return int(math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100)

    return (int(((entry[3]/10)/entry[2])*math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100))

def displayAllValues(dbinstance):

    for entry in searchTable(dbinstance, "stockinfo"): 
        value = estimateValue(dbinstance, '\'' + entry[0] + '\'')
        print(f"{entry[0]}: {value}")