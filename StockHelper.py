from StockProjector import retrieveProjections
from MySQLcommands import *
from Database import *


def main():

    # Insert your MySQL database credentials to use certain features (optional)
    db = initDatabase("INSERT HOSTNAME", "INSERT USERNAME", "INSERT PASSWORD")

    if (db != None): retrieveProjections(db)
    else: retrieveProjections()
    

if __name__ == "__main__": main()
