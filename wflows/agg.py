#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect('host=localhost dbname=tpch user=p2d2 password=p2d2')

df = pd.read_sql_query('SELECT * FROM customer', conn)
proj1 = df.loc[:,['c_custkey', 'c_nationkey', 'c_acctbal']]
proj2 = df.loc[:,['c_custkey', 'c_nationkey', 'c_mktsegment', 'c_acctbal']]
nogroup2 = proj1.agg({'c_nationkey': [np.sum,np.max], 'c_acctbal': [np.max]})

maxi = proj1.max().to_frame().T
mean = proj1.mean().to_frame().T 
mini = proj1.min().to_frame().T 
sumi = proj1.sum().to_frame().T  
std = proj1.std().to_frame().T   
var = proj1.var().to_frame().T   
median = proj1.median().to_frame().T
mode = proj1.mode().head(1)
sample1 = proj1.sample(1)
sample2 = proj1.sample(10)

gmaxi =proj1.groupby(['c_nationkey']).max()
gmean =proj1.groupby(['c_nationkey']).mean() 
gmini =proj1.groupby(['c_nationkey']).min()  
gsumi =proj1.groupby(['c_nationkey']).sum()   
gstd = proj1.groupby(['c_nationkey']).std()   
gvar = proj1.groupby(['c_nationkey']).var()   
#gmode =proj1.groupby(['c_nationkey']).mode() #can't mode with groupby
gmedian =proj1.groupby(['c_nationkey']).median()
gsample =proj1.groupby(['c_nationkey']).sample() 

ggmaxi= proj2.groupby(['c_nationkey', 'c_mktsegment']).max()
ggmean= proj2.groupby(['c_nationkey', 'c_mktsegment']).mean()
ggmini= proj2.groupby(['c_nationkey', 'c_mktsegment']).min()
ggsumi= proj2.groupby(['c_nationkey', 'c_mktsegment']).sum()
ggstd= proj2.groupby(['c_nationkey', 'c_mktsegment']).std()
ggvar= proj2.groupby(['c_nationkey', 'c_mktsegment']).var()
#ggmode= proj2.groupby(['c_nationkey', 'c_mktsegment']).mode #can't mode with groupby
ggmedian=proj2.groupby(['c_nationkey', 'c_mktsegment']).median()
ggsample=proj2.groupby(['c_nationkey', 'c_mktsegment']).sample()

print('maxi')
print(maxi)
print('mean')
print(mean)
print('mini')
print(mini)
print('sumi')
print(sumi)
print('std')
print(std)
print('var')
print(var)
print('median')
print(median)
print('mode')
print(mode)
print('sample1')
print(sample1)
print('sample2')
print(sample2)


print('gmaxi')
print(f'{gmaxi}')
print('gmean')
print(f'{gmean}')
print('gmini')
print(f'{gmini}')
print('gsumi')
print(f'{gsumi}')
print('gstd')
print(f'{gstd}')
print('gvar')
print(f'{gvar}')
print('gmedian')
print(f'{gmedian}')
print('gsample')
print(f'{gsample}')

print('ggmaxi')
print(f'{ggmaxi}')
print('ggmean')
print(f'{ggmean}')
print('ggmini')
print(f'{ggmini}')
print('ggsumi')
print(f'{ggsumi}')
print('ggstd')
print(f'{ggstd}')
print('ggvar')
print(f'{ggvar}')
print('ggmedian')
print(f'{ggmedian}')
print('ggsample')
print(f'{ggsample}')
