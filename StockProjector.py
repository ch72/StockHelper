from polygon import RESTClient
import math
import requests
from MySQLcommands import *
from Database import estimateValue
from time import sleep

# -------------------------------------------------------------------------------
# Stock Projector
#
# Inputs: Stock ticker, projected growth rate, and optimism level
#
# Prints: A table containing various stock prices based on different
# P/S ratios and growth rates after 5 years
# -------------------------------------------------------------------------------

def retrieveProjections(key, dbinstance=None):

    restart = 'y'

    # while loop allows user to restart program
    # Note: If too many API calls are made in a short timeframe, APIs calls and subsequent code may fail
    while (restart == 'y'):

        stock = input("Which stock projection are you looking for?\n").upper()

        price, marketCap, revenue, grossMargin = grabInfo(stock, key)

        if (float(marketCap) < 0 or float(revenue) < 0 or float(price) < 0):
            print ("Something went wrong.")
            exit(1)

        priceToSales = float(marketCap)/float(revenue)

        #print("Revenue (in billions): " + str(revenue / 1000000000))
        #print("Market Cap (in billions): " + str(marketCap / 1000000000))

        growth = input("What is the projected growth rate?\n")
        #numOfYears = input("Over how many years?\n")
        optimism = input("Optimistic, fair, or pessimistic (O/F/P)?\n").upper()

        # Optimism determines how high/low the table's P/S ratios will go for calulations
        # Growth rates are unchanged by optimism because user can manually change growth if they want more optimism/pessimism
        if (optimism == "O"): projections(float(price), float(priceToSales), int(growth), 5, 5, "O")
        elif (optimism == "P"): projections(float(price), float(priceToSales), int(growth), 5, 5, "P")
        else: projections(float(price), float(priceToSales), int(growth), 5, 5, "F")

        # If stock is not in the database, add it to the row
        if (dbinstance != None and searchTable(dbinstance, "stockinfo", condition=f"ticker='{stock}'") == []):
            insertRow(dbinstance, 'stockinfo', [stock, price, priceToSales, growth, grossMargin])
        else: # Otherwise, update row
            deleteRow(dbinstance, 'stockinfo', condition=f'ticker=\'{stock}\'')
            insertRow(dbinstance, 'stockinfo', [stock, price, priceToSales, growth, grossMargin])
                

        restart = input("Would you like to run it again (y/n)?\n")  # Allows user to restart the program if desired

# Retrieves stock price, current market cap, last year's revenue, and gross margin from Polygon API
def grabInfo(stock, key):

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
            
        #Retrieve stock price
        price = -1
        try: resp = client.stocks_equities_previous_close(stock)
        except: 
            print (stock + " is not a ticker")
            exit(1)
        if(resp.status == "OK"): price = resp.results[0]['c']

        # Retrieve market cap
        try: resp = client.reference_tickers_v3("https://api.polygon.io/v3/reference/tickers/" + stock + "?apiKey=" + key)
        except: print (stock + " is not a ticker")
        marketCap = -1
        if (resp.status == "OK"): marketCap = resp.results['market_cap']
        
        if (float(marketCap) < 0): 
            print ("Something went wrong with data retrieval.")
            exit(1)

        # Retrieve revenue (sales)
        revenue = -1
        grossMargin = -1
        try: 
            resp = requests.get('https://api.polygon.io/vX/reference/financials?ticker=' + stock + '&timeframe=annual&apiKey=' + key)
            revenue = resp.json()['results'][0]['financials']['income_statement']['revenues']['value']
            grossMargin = float(int(resp.json()['results'][0]['financials']['income_statement']['gross_profit']['value']) / int(revenue))
        except: print ("Something went wrong with Polygon")

        return price, marketCap, revenue, grossMargin

# Creates a table that projects future stock prices based on valuation changes and growth rates
# Valuation in this case are the P/S ratios
def projections(stockPrice, valuation, growthRate, rows, columns, optimism, years=5):

    unmodifiedPrice = stockPrice

    # Rounds valuation and updates stock price to reflect rounded valuation (to improve accuracy)
    stockPrice = (round(valuation) * stockPrice) / valuation
    valuation = round(valuation)

    if (valuation == 0): return "Something Went Wrong"

    # TODO: Make these variables scale to the size of growth rate
    growthDiff = 5
    valDiff = int(valuation / rows)
    if (valDiff <= 0):
        valDiff = valuation / rows

    leftCol = int(-1 * int(columns / 2))    # All left/right variables are casted to int 
    rightCol = int(columns + leftCol)       # to ensure no decimals cause errors

    # Valuations used for calculations will all be greater than or equal to current stock valuation
    if (optimism == "O"):    
        leftRow = 0
        rightRow = rows

    # Valuations used for calculations will all be less than or equal to current stock valuation
    elif (optimism == "P"):    
        leftRow = -1 * rows + 1
        rightRow = 1

    # Valuations used for calculations will be both greater than and less than current stock valuation
    else:
        leftRow = int(-1 * int(rows/2))
        rightRow = int(rows + leftRow)

    print (f"Current Price (rounded): ${round(unmodifiedPrice)}")

    # Creates price matrix that contains values from calcFutureStockPrice
    # using stock price, valuation +/- valDiff, and growth rate +/- growthDiff
    priceMatrix = [[calcFuturePrice(stockPrice, valuation, valuation+valDiff*j, growthRate+growthDiff*i, years) \
    for i in range(leftCol, rightCol)] for j in range(leftRow, rightRow)]
    
    # Creates matrix of percentages to illustrate whether stock goes up or down
    # Represented as a number (0.8 = -20% and 1.35 = +35%)
    #priceMatrix = [[calcFutureGains(valuation, valuation+valDiff*j, growthRate+growthDiff*i, years) \
    #for i in range(leftCol, rightCol)] for j in range(leftRow, rightRow)]

    generateHeader(growthRate, growthDiff, leftCol, rightCol)
    
    # Generates body underneath the header
    for i in range(leftRow, rightRow): 
        print("".ljust(10) + "|")
        isMiddle = (i == leftRow + 1)   
        print(generateLeftOfRow(valuation + (valDiff*i), isMiddle), generateValuesForRow(priceMatrix[i - leftRow]))
    print("".ljust(10) + "|")

# Generates a single block, which is each entry in the table
# Meant for the right side of the "|"
def generateBlock(value): return str(value).ljust(8)

# Generates header of table (growth rates)
def generateHeader(growthRate, growthDiff, leftCol, rightCol):

    print("".ljust(10) + "|" + "Growth Rates".rjust(17))
    print("".ljust(10) + "|")
    line = "".ljust(10) + "|" + "".ljust(2)
    for i in range(leftCol, rightCol): line += generateBlock(str(growthRate + (growthDiff * i)) + "%")
    print(line)
    print("-" * (11 + (rightCol-leftCol)*8))

# Generates the left side of the "|" in the table for a single row of values (P/S ratios)
def generateLeftOfRow(priceToSales, isMiddle):

    priceToSales = str(round(priceToSales, 1))
    if (isMiddle): row = "".ljust(1) + "P/S".ljust(5) + priceToSales.rjust(3) + "".ljust(1) + "|"
    else: row = "".ljust(6) + priceToSales.rjust(3) + "".ljust(1) + "|"
    return row

# Generates the right side of the "|" in the table for a single row of values (possible stock prices/gains)
def generateValuesForRow(values): 
    
    row = "".ljust(1)
    for i in range(len(values)): row += generateBlock(values[i])
    return row

# Calculates a stock price prediction based on valuations and growth rates
# Growth rate should be inputted as a whole number (30 = 30%)
def calcFuturePrice(stockPrice, oldVal, newVal, growth, years):

    if (newVal > 0): return str(round(((float(newVal)/float(oldVal))*math.pow(1 + int(growth)/100, int(years))) * stockPrice))
    return 0

# Calculates potential gain of a stock as a percentage based on valuation and growth rates
def calcFutureGains(oldVal, newVal, growth, years):

    #print (f"New Value: {newVal} and Old Value: {oldVal}")
    if (newVal > 0): return str(round(((float(newVal)/float(oldVal))*math.pow(1 + int(growth)/100, int(years))), 2))
    return 0

# Refreshes database info with new stock price, valuation, and gross margin (if needed)
def refreshDatabaseInfo(dbinstance, key):

    print ("Updating database with today's new stock price", end="", flush=True)

    databaseEntries = searchTable(dbinstance, "stockinfo")

    print(f"Updating {len(databaseEntries)} database entries...")

    for entry in databaseEntries:

        stock = entry[0]
        growthRate = entry[3]
        price, marketCap, revenue, grossMargin = grabInfo(stock, key)
        deleteRow(dbinstance, 'stockinfo', condition=f'ticker=\'{stock}\'')
        insertRow(dbinstance, 'stockinfo', [stock, price, marketCap/revenue, growthRate, grossMargin])
        print(f"{entry[0]} was updated...")
        sleep(15)        # Sleep is needed to stay under API call limit per minute (causes failure)
    
    print ("Update complete!")