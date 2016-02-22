#!/usr/bin/python

from bursa.db import db
from bursa.models import Company, MarketCap, StakeHolders, Management, FinancialReport

def main():
    db.connect()
    db.database.create_tables([Company, MarketCap, StakeHolders, Management, FinancialReport])

if __name__ == "__main__":
    main()
