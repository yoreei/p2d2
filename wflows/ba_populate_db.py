#!/usr/bin/env python
# coding: utf-8

# Creates relational tables with sqlalchemy to accomodate stock data from yfinance
# Test them with a little query from yfinance
import pandas as pd
import numpy as np
import sqlalchemy as sa
import yfinance
import IPython
import csv

#reads snp100.csv
#downloads data from yfinance
#pushes data to local mariadb

YF_INTERVAL = '30m' #1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
CSV_SAMPLE = 5 #False to disable cutoff, int to enable
engine = sa.create_engine('mysql+pymysql://mydeb:password@localhost/satest', echo=True)

def get_snp100():
    with open('snp100.csv', newline='') as f:
        reader = csv.reader(f)
        stock_names = list(reader)
        stock_names = stock_names[0] #the file has only 1 line
    if CSV_SAMPLE is not False:        
        stock_names = stock_names[:CSV_SAMPLE]
    return stock_names

def download_and_push_stock(stock_name):
    stock_data = yfinance.download(stock_name,
                           period= "2d",
                           interval = YF_INTERVAL,
                           group_by="ticker")
    if stock_data.empty:
        return False 

    stock_data.index.names=['Datetime']
    stock_data.to_sql(stock_name, engine, if_exists='replace')

    return True

def main():
    # https://docs.sqlalchemy.org/en/13/core/metadata.html
    #metadata = sa.MetaData()
    #stock_data=stock_data.stack(level=0)

    stock_names = get_snp100()
    available_names = []
    for stock_name in stock_names:
        success = download_and_push_stock(stock_name)
        if success:
            available_names += [stock_name]

    print (available_names)
    available_names_s = pd.Series(available_names, name='STOCK_NAMES')
    available_names_s.to_sql('STOCK_NAMES', engine, index=False,  if_exists='replace')
    IPython.embed();exit()

if __name__=='__main__':
    main()

#sql_DF = pd.read_sql_table("mystocks",
#                           parse_dates=['Datetime'],
#                           index_col=['Datetime','Company'] ,
#                           con=engine)
#sql_DF
