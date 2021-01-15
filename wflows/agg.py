#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

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

gmaxi =proj2.groupby(['c_nationkey']).max()
gmean =proj2.groupby(['c_nationkey']).mean() 
gmini =proj2.groupby(['c_nationkey']).min()  
gsumi =proj2.groupby(['c_nationkey']).sum()   
gstd = proj2.groupby(['c_nationkey']).std()   
gvar = proj2.groupby(['c_nationkey']).var()   
gmode =proj2.groupby(['c_nationkey']).mode()   
gmedian =proj2.groupby(['c_nationkey']).median()
gsample =proj2.groupby(['c_nationkey']).sample() 
"""

ggmaxi =  proj2.groupby(['c_nationkey', 'c_mktsegment']).max
ggmean =  proj2.groupby(['c_nationkey', 'c_mktsegment']).mean   
ggmini =  proj2.groupby(['c_nationkey', 'c_mktsegment']).min    
ggsumi =  proj2.groupby(['c_nationkey', 'c_mktsegment']).sum    
ggstd =   proj2.groupby(['c_nationkey', 'c_mktsegment']).std    
ggvar =   proj2.groupby(['c_nationkey', 'c_mktsegment']).var    
ggmode =  proj2.groupby(['c_nationkey', 'c_mktsegment']).mode   
ggmedian =proj2.groupby(['c_nationkey', 'c_mktsegment']).median 
ggsample =proj2.groupby(['c_nationkey', 'c_mktsegment']).sample 
"""

print('maxi')
print(maxi)
print('mean')
print(mean   )
print('mini') 
print(mini   )
print('sumi'   )
print(sumi   )
print('std'    )
print(std    )
print('var'  )
print(var    )
print('median'  )
print(median  )
print('mode'   )
print(mode   )
print('sample1'  )
print(sample1  )
print('sample2'  )
print(sample2  )


print(f'{gmaxi=}')
print(f'{gmean=}')
print(f'{gmini=}')
print(f'{gsumi=}')
print(f'{gstd=}')
print(f'{gvar=}')
print(f'{gmode=}')
print(f'{gmedian=}')
print(f'{gsample=}')
"""

print(f'{ggmaxi=}')
print(f'{ggmean=}')
print(f'{ggmini=}')
print(f'{ggsumi=}')
print(f'{ggstd=}')
print(f'{ggvar=}')
print(f'{ggmode=}')
print(f'{ggmedian=}')
print(f'{ggsample=}')
"""
