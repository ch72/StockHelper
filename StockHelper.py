from StockProjector import retrieveProjections, refreshDatabaseInfo
from MySQLcommands import *
from Database import *


def main():

    key = "" # <-INSERT POLYGON API KEY HERE

    # region to hide MySQL credentials
    # Insert your MySQL database credentials to use certain features (optional)
    db = initDatabase("INSERT HOSTNAME", "INSERT USERNAME", "INSERT PASSWORD")
    # endregion

    if (db != None): retrieveProjections(key, dbinstance=db)
    else: retrieveProjections(key)

if __name__ == "__main__": main()
