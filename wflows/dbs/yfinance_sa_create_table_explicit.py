#!/usr/bin/env python
# coding: utf-8

# Creates relational tables with sqlalchemy to accomodate stock data from yfinance
# Test them with a little query from yfinance
import pandas as pd
import numpy as np
import sqlalchemy as sa
import yfinance

engine = sa.create_engine('mysql+pymysql://mydeb:mydeb@localhost/satest', echo=True)
# https://docs.sqlalchemy.org/en/13/core/metadata.html
metadata = sa.MetaData()

user = sa.Table('mystocks', metadata,
    sa.Column('Datetime', sa.DateTime(), primary_key=True),
    sa.Column('Company', sa.String(16), primary_key=True),
    sa.Column('Open', sa.Float()),
    sa.Column('Low', sa.Float()),
    sa.Column('High', sa.Float()),
    sa.Column('Close', sa.Float()),
    sa.Column('Adj Close', sa.Float()),
    sa.Column('Volume', sa.Float()),
    sa.UniqueConstraint('Datetime', 'Company', name='uix_1')
)

metadata.create_all(engine, checkfirst=True)
# # Test
stockData = yfinance.download(["EBAY","AAPL","MSFT"],
                           period= "2d",
                           interval = "5m",
                           group_by="ticker")

stockData=stockData.stack(level=0)
stockData.index.names=['Datetime','Company']

firstData=stockData.head(2)
secondData=stockData[2:3]

firstData

secondData

firstData.to_sql("mystocks",engine, if_exists='append')

secondData.to_sql("mystocks",engine, if_exists='append')

sql_DF = pd.read_sql_table("mystocks",
                           parse_dates=['Datetime'],
                           index_col=['Datetime','Company'] ,
                           con=engine)

sql_DF
