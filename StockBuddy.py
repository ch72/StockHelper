from polygon import RESTClient
import math
import re

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

    key = ""

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
            
            stock = input("Which stock projection are you looking for?\n")
            resp = client.stocks_equities_daily_open_close(stock, "2022-03-24")
            price = resp.close

            try: resp = client.reference_tickers_v3("https://api.polygon.io/v3/reference/tickers/" + stock + "?apiKey=" + key)
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

            # Retrieve revenue (sales)
            revenue = -1
            for data in re.split(",", str(re.sub(" ", "", str(resp.results)))):
                if (data[0:11] == "\'revenues\':"): 
                    revenue = data[11:]
                    break
            if (float(revenue) < 0):
                print ("Something went wrong with data retrieval.")
                exit(2)

            #print("Market Cap: " + marketCap)
            #print("Revenue: " + revenue)
            #print((float(marketCap))/(float(revenue)))

            projections(price, round(float(marketCap)/float(revenue))/4, 10)


# Creates the matrix that contains possible future stock prices
def projections(stockPrice, valuation, growthRate):

    # TODO: Make these variables scale to the size of valuation and growth rate
    growthDiff = 10
    valDiff = 5

    priceMatrix = [[calcFuturePrice(stockPrice, valuation, valuation+valDiff*j, growthRate+growthDiff*i) \
    for i in range(-1, 2)] for j in range(-1, 2)]

    # Creates matrix using values calculated in price matrix
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

# Calculates a stock price prediction based on valuations and growth rates
# Growth rate should be inputted as a whole number (30 = 30%)
def calcFuturePrice(stockPrice, oldVal, newVal, growth, years = 5):

    if (newVal > 0): return str(round(((int(newVal)/int(oldVal))*math.pow(1 + int(growth)/100, years)) * stockPrice))

main()