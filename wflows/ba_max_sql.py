#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sqlalchemy as sa
import IPython

engine = sa.create_engine('mysql+pymysql://mydeb:password@localhost/satest', echo=True)

def main():
    
    stock_names = pd.read_sql('SELECT * FROM STOCK_NAMES sn LIMIT 1', engine)
    stock_name = stock_names.iloc[0].item() #'AAPL' 
    
    date_from = '2020-08-27 00:00:00'
    date_to = '2020-08-27 23:59:59' 
    stock_data = pd.read_sql(f'SELECT MAX(High) FROM {stock_name} WHERE Datetime BETWEEN \'{date_from}\' and \'{date_to}\'', engine) 
    print(stock_data.loc[0].item())

    #IPython.embed();exit()

if __name__=='__main__':
    main()
