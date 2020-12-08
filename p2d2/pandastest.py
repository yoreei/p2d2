import pandas as pd
import numpy as np
import pgconn

def design():
    conn = pgconn.get() #gives us a connection to PostgreSQL.
    a = pd.read_sql_query('SELECT * FROM customer', conn)
    #mask = a['c_acctbal'] < 800
    a.loc[a['c_acctbal'] < 800, 'c_acctbal'] = 42
    a.loc[a.loc[:,'c_acctbal']>800,['c_acctbal','c_custkey']]=52

    print(a)

def fromdocs():
    dfc = pd.DataFrame({'a': ['one', 'one', 'two',
                              'three', 'two', 'one', 'six'],
                        'c': np.arange(7)})
    print(dfc)
    #dfd = dfc.copy()

    mask = dfc['a'].str.startswith('o')

    dfc.loc[mask, 'c'] = 42
    print (dfc)


conn = pgconn.get() #gives us a connection to PostgreSQL. 
a = pd.read_sql_query('SELECT * FROM customer', conn)
p = a.loc[:,'c_custkey'] # probably a view but we take it as a copy
cop = a.loc[:,['c_custkey','c_name','c_acctbal']].copy()
s = a.loc[a.loc[:,'c_acctbal']<800]
a.loc[a['c_acctbal'] < 800, 'c_acctbal'] = 4

