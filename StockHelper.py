from StockProjector import retrieveProjections, refreshDatabaseInfo
from MySQLcommands import *
from Database import *


def main():

    key = "" # <-INSERT POLYGON API KEY HERE

    # region to hide MySQL credentials on VSCode
    # Insert your MySQL database credentials to use certain features (optional)
    db = initDatabase("INSERT HOSTNAME", "INSERT USERNAME", "INSERT PASSWORD")
    # endregion

    # OPTIONS: 
    # update - update stock database with current price and company metrics
    # calculate - calculate "rating" for each stock in database and lists the "risk" of the investment in parentheses
    # table - creates table for given stock and adds stock to database
    # delete - deletes row from database (command only available if MySQL database is supplied)
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
        elif (request == "d" or request == "delete"):
            if (db == None): 
                print ("Can't delete. No database supplied.")
                break
            elif (deleteRow(db, "stockinfo", "ticker = \'" + input("Enter ticker of stock to delete.\n") + "\'", dbname="stockdatabase")):
                print ("All stocks with inputted ticker were deleted.")
        elif (request == "e" or request == "exit"):
            break
        else:
            print ("That's not a valid option! Valid options are update, calculate, table, or exit.")

if __name__ == "__main__": main()
