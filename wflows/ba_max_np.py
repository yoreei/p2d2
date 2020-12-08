#!/usr/bin/env python

import pandas as pd
import numpy as np
import sqlalchemy as sa
import IPython

engine = sa.create_engine('mysql+pymysql://mydeb:password@localhost/satest', echo=True)

def main():
    
    stock_names = pd.read_sql("SELECT * FROM STOCK_NAMES", engine)
    stock_name = stock_names.iloc[0].item() #'AAPL' 
    
    date_from = '2020-08-27 00:00:00'
    date_to = '2020-08-27 23:59:59' 
    stock_data = pd.read_sql(f'SELECT * FROM {stock_name}', engine, 'Datetime') 
    today_data = stock_data.loc[date_from : date_to]
    today_data_np = today_data.to_numpy()
    highs = today_data_np[:,0]
    max_high = np.amax(highs)
    print(max_high)

    #IPython.embed();exit()

if __name__=='__main__':
    main()
