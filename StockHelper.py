from StockProjector import retrieveProjections, refreshDatabaseInfo
from MySQLcommands import *
from Database import *


def main():

    key = "" # <-INSERT POLYGON API KEY HERE

    # region to hide MySQL credentials
    # Insert your MySQL database credentials to use certain features (optional)
    db = initDatabase("INSERT HOSTNAME", "INSERT USERNAME", "INSERT PASSWORD")
    # endregion

    # OPTIONS: 
    # update - update stock database with current price and company metrics
    # calculate - calculate "rating" for each stock in database 
    # table - creates table for given stock and adds stock to database
    # exit - exit the program
    while (True):
        
        request = input("What would you like to do today?\n").lower()

        if (request == "u" or request == "update"):
            refreshDatabaseInfo(db, key)
            break
        elif (request == "c" or request == "calculate"):
            displayAllValues(db, "G")
            break
        elif (request == "t" or request == "table"):
            if (db != None): retrieveProjections(key, dbinstance=db)
            else: retrieveProjections(key)
            break
        elif (request == "e" or request == "exit"):
            break
        else:
            print ("That's not a valid option! Valid options are update, calculate, table, or exit.")

if __name__ == "__main__": main()
