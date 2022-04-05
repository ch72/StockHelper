from time import timezone
from polygon import RESTClient
import math
import requests

# -------------------------------------------------------------------------------
# Stock Projector
#
# Inputs: Stock ticker, projected growth rate, and optimism level
#
# Prints: A table containing various stock prices based on different
# P/S ratios and growth rates after 5 years
# -------------------------------------------------------------------------------

def main():

    key = ""

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
            
            #Retrieve stock price
            stock = input("Which stock projection are you looking for?\n").upper()
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

            # TODO: Handle errors if api retrieval fails or retrieves wrong info
            # Retrieve revenue (sales)
            revenue = -1
            try: resp = requests.get('https://api.polygon.io/vX/reference/financials?ticker=' + stock + '&timeframe=annual&apiKey=' + key)
            except: print ("Something went wrong with Polygon")
            revenue = resp.json()['results'][0]['financials']['income_statement']['revenues']['value']

            if (float(marketCap) < 0 or float(revenue) < 0 or float(price) < 0):
                print ("Something went wrong.")
                exit(1)

            priceToSales = float(marketCap)/float(revenue)

            #print("Revenue (in billions): " + str(revenue / 1000000000))
            #print("Market Cap (in billions): " + str(marketCap / 1000000000))

            growth = input("What is the projected growth rate?\n")
            #numOfYears = input("Over how many years?\n")
            optimism = input("Optimistic, fair, or pessimistic (O/F/P)?\n").upper()

            if (optimism == "O"): projections(float(price), float(priceToSales), int(growth), 5, 5, "O")
            elif (optimism == "P"): projections(float(price), float(priceToSales), int(growth), 5, 5, "P")
            else: projections(float(price), float(priceToSales), int(growth), 5, 5, "F")


#TODO: Fix calculations for P/S of anything close to 0 (1, 2, 0.5, etc)
# Creates a table that projects future stock prices based on valuation changes and growth rates
def projections(stockPrice, valuation, growthRate, rows, columns, optimism, years=5):

    # Rounds valuation and updates stock price to reflect rounded valuation (to improve accuracy)
    stockPrice = (round(valuation) * stockPrice) / valuation
    valuation = round(valuation)

    if (valuation == 0): return "Something Went Wrong"

    # TODO: Make these variables scale to the size of growth rate
    growthDiff = 5
    valDiff = int(valuation / rows)
    if (valDiff <= 0):
        valDiff = valuation / rows

    if (optimism == "O"):
        leftCol = 0
        rightCol = columns
        leftRow = 0
        rightRow = rows

    elif (optimism == "P"):
        leftCol = -1 * columns + 1
        rightCol = 1
        leftRow = -1 * rows + 1
        rightRow = 1

    else:
        leftCol = int(-1 * int(columns / 2))    # All left/right variables are casted to int 
        rightCol = int(columns + leftCol)       # to ensure no decimals cause errors
        leftRow = int(-1 * int(rows/2))
        rightRow = int(rows + leftRow)

    # Creates price matrix that contains values from calcFutureStockPrice
    # using stock price, valuation +/- valDiff, and growth rate +/- growthDiff
    priceMatrix = [[calcFuturePrice(stockPrice, valuation, valuation+valDiff*j, growthRate+growthDiff*i, years) \
    for i in range(leftCol, rightCol)] for j in range(leftRow, rightRow)]

    generateHeader(growthRate, growthDiff, leftCol, rightCol)
    
    # Generates body underneath the header
    for i in range(leftRow, rightRow): 
        print("".ljust(10) + "|")
        isMiddle = (i == int((rightRow + leftRow)/2))   
        print(generateLeftOfRow(valuation + (valDiff*i), isMiddle), generateValuesForRow(priceMatrix[i - leftRow]))
    print("".ljust(10) + "|")

# Generates a single block, which is each entry in the table
# Meant for the right side of the "|"
def generateBlock(value): return str(value).ljust(8)

# Generates header of table
def generateHeader(growthRate, growthDiff, leftCol, rightCol):

    print("".ljust(10) + "|" + "Growth Rates".rjust(17))
    print("".ljust(10) + "|")
    line = "".ljust(10) + "|" + "".ljust(2)
    for i in range(leftCol, rightCol): line += generateBlock(str(growthRate + (growthDiff * i)) + "%")
    print(line)
    print("-" * (11 + (rightCol-leftCol)*8))

# Generates the left side of the "|" in the table for a single row of values
def generateLeftOfRow(priceToSales, isMiddle):

    priceToSales = str(priceToSales)
    if (isMiddle): row = "".ljust(1) + "P/S".ljust(5) + priceToSales.rjust(3) + "".ljust(1) + "|"
    else: row = "".ljust(6) + priceToSales.rjust(3) + "".ljust(1) + "|"
    return row

# Generates the right side of the "|" in the table for a single row of values
def generateValuesForRow(values): 
    
    row = "".ljust(1)
    for i in range(len(values)): row += generateBlock(values[i])
    return row


# Calculates a stock price prediction based on valuations and growth rates
# Growth rate should be inputted as a whole number (30 = 30%)
def calcFuturePrice(stockPrice, oldVal, newVal, growth, years):

    if (newVal > 0): return str(round(((int(newVal)/int(oldVal))*math.pow(1 + int(growth)/100, int(years))) * stockPrice))
    return 0

if __name__ == "__main__": main()