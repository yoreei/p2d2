#!/usr/bin/env python
# coding: utf-8

# Extracts date of first entry, date of last entry and number of rows from persistency_test.db
import pandas as pd
import numpy as np
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import yfinance

engine = sa.create_engine('mysql+pymysql://mydeb:mydeb@localhost/satest', echo=False)
meta = sa.MetaData()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.metadata.reflect(engine)

Session = sessionmaker(bind=engine)
session = Session()

mystocksTable = sa.Table('myStocks', meta, autoload=True, autoload_with=engine)

class myStocks(Base):
    __table__ = mystocksTable
    def __repr__(self):
        return "hahahahahaha"

firstElem=session.query(myStocks).order_by(myStocks.Datetime.desc()).first()
lastElem=session.query(myStocks).order_by(myStocks.Datetime.desc()).first()
count = session.query(myStocks).count()
print("first entry is dated "+str(firstElem.Datetime))
print("last entry is dated "+str(lastElem.Datetime))
print("number of rows: "+str(count))

#import datetime as dt
#my_time = dt.datetime(2020,3,6,9,30,0)
#
#print(my_time.strftime("%Y-%m-%d %H:%M:%S"))
#
#print (session.query(sa.exists().where(myStocks.Datetime == my_time)).scalar())



