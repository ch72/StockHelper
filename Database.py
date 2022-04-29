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
def estimateValue(dbinstance, ticker, mindset=None):

    entry = searchTable(dbinstance, "stockinfo", condition=f'ticker={ticker}')[0]

    #if (entry[3] < 10): 
        #if (entry[2] > 1): return str(int((1/entry[2])*math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100)) + " (adjusted)"
        #else: return str(int(math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100)) + " (adjusted)"

    #return (int(((entry[3]/10)/entry[2])*math.pow(1 + float(entry[3]/100), 5)*(entry[4])*100))
    if (mindset=="V"): 
        if (entry[2] >= 1): return 2*int(((math.pow(1 + float(entry[3]/100), 5))/entry[2])*entry[4]*100)
        else: return 2*int((math.pow(1 + float(entry[3]/100), 5))*entry[4]*100)
    else: return int(((math.pow(1 + float(entry[3]/100), 5))/entry[2])*(math.pow(1 + float(entry[3]/100), 5))*entry[4]*100)

def displayAllValues(dbinstance, mindset=None):

    for entry in searchTable(dbinstance, "stockinfo"): 
        
        if (mindset == "V"): value = estimateValue(dbinstance,'\'' + entry[0] + '\'', "V")
        else: value = estimateValue(dbinstance, '\'' + entry[0] + '\'', "G")

        risk = 0

        # Stock is riskier if valuation is high
        if (entry[2]*(1/entry[4]) > 30): risk += 3
        elif (entry[2]*(1/entry[4]) > 15): risk += 2
        elif (entry[2]*(1/entry[4]) > 5): risk += 1

        # Stock if riskier if growth rate is negative or 0
        if (entry[3] < 0): risk += 1

        # TODO (?): Increment risk if stock has low gross margins and is unprofitable
        # TODO (?): Increment risk if stock has a ton of debt on the books

        if (risk <= 0): risk = "(Low)"
        elif (risk == 1): risk = "(Medium)"
        elif (risk == 2): risk = "(High)"
        else: risk = "(Very High)"

        print((str(entry[0]) + ": ").ljust(7) + str(value).ljust(5) + risk)