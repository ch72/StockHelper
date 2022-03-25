from polygon import RESTClient
from datetime import date
import time
import math
import re
import requests

# -------------------------------------
# Stock Projector
#
# Inputs: Ticker
#
# Output: A matrix containing various
# stock prices based on different
# P/S ratios and growth rates
# -------------------------------------

# TODO: Find source of wrong values (wrong API numbers or regex is pulling the wrong numbers)
def main():

    key = "insert key here"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
            
            stock = input("Which stock projection are you looking for?\n")

            try: resp = client.reference_tickers_v3("https://api.polygon.io/v3/reference/tickers/" + stock + "?apiKey=insert key here")

            except: print (" is not a ticker")

            # Retrive market cap
            marketCap = -1
            for data in re.split(",", str(re.sub(" ", "", str(resp.results)))):
                if (data[0:13] == "\'market_cap\':"): 
                    marketCap = data[13:]
                    break
            if (float(marketCap) < 0): 
                print ("Something went wrong with data retrieval.")
                exit(1)
            
            # TODO: Learn query parameters
            #queryParams = {
             #   'ticker': 'CRM',
             #   'timeframe': 'annual',
             #   'apiKey': 'insert key here'
            #}

            try: resp = client.reference_stock_financials(stock)
            except: print ("Something went wrong with Polygon")

            revenue = -1
            for data in re.split(",", str(re.sub(" ", "", str(resp.results)))):
                if (data[0:11] == "\'revenues\':"): 
                    revenue = data[11:]
                    break
            if (float(revenue) < 0):
                print ("Something went wrong with data retrieval.")
                exit(2)

            print("Market Cap: " + marketCap)
            print("Revenue: " + revenue)
            print((float(marketCap))/(float(revenue)))


# Creates the matrix that contains possible future stock prices
def projections(stockPrice, valuation, growthRate):

    growthDiff = 10
    valDiff = 5

    priceMatrix = [[calcFuturePrice(stockPrice, valuation, valuation+valDiff*j, growthRate+growthDiff*i) \
    for i in range(-1, 2)] for j in range(-1, 2)]

    #print(str(calcFuturePrice(stockPrice, valuation, valuation-valDiff, growthRate-growthDiff)))

    print("".ljust(10) + "|" + "Growth Rates".rjust(17))
    print("".ljust(10) + "|")
    print("".ljust(10) + "|" + "".ljust(2) + (str(growthRate - growthDiff) + "%").ljust(8) + (str(growthRate) + "%").ljust(8) \
        + (str(growthRate + growthDiff) + "%").ljust(8))
    print("-" * 40)
    print("".ljust(10) + "|")
    print("".ljust(6) + str(round(valuation - valDiff)).rjust(3) + "".ljust(1) + "|" + "".ljust(2) + \
        priceMatrix[0][0].ljust(8) + priceMatrix[0][1].ljust(8) + priceMatrix[0][2].ljust(8))
    print("".ljust(10) + "|")
    print("".ljust(1) + "P/S".ljust(5) + str(round(valuation)).rjust(3) + "".ljust(1) + "|" + "".ljust(2) + \
        priceMatrix[1][0].ljust(8) + priceMatrix[1][1].ljust(8) + priceMatrix[1][2].ljust(8))
    print("".ljust(10) + "|")
    print("".ljust(6) + str(round(valuation + valDiff)).rjust(3) + "".ljust(1) + "|" + "".ljust(2) + \
        priceMatrix[2][0].ljust(8) + priceMatrix[2][1].ljust(8) + priceMatrix[2][2].ljust(8))

# Growth rate should be inputted as a whole number (30 = 30%)
def calcFuturePrice(stockPrice, oldVal, newVal, growth, years = 5):

    if (newVal > 0): return str(round(((int(newVal)/int(oldVal))*math.pow(1 + int(growth)/100, years)) * stockPrice))

main()