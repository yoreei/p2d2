#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

df2 = pd.read_sql_query('SELECT * FROM customer', conn)
proj2 = df2.loc[:,['c_custkey', 'c_nationkey', 'c_mktsegment', 'c_acctbal']]

maxi = proj2.max.to_frame().T
mean = proj2.mean.to_frame().T 
mini = proj2.min.to_frame().T 
sumi = proj2.sum.to_frame().T  
std = proj2.std.to_frame().T   
var = proj2.var.to_frame().T   
mode = proj2.mode.to_frame().T  
median = proj2.median.to_frame().T
sample = proj2.sample.to_frame().T

gmaxi =    proj2.groupby('c_nationkey').max
gmean =    proj2.groupby('c_nationkey').mean   
gmini =    proj2.groupby('c_nationkey').min    
gsumi =    proj2.groupby('c_nationkey').sum    
gstd =     proj2.groupby('c_nationkey').std    
gvar =     proj2.groupby('c_nationkey').var    
gmode =    proj2.groupby('c_nationkey').mode   
gmedian =    proj2.groupby('c_nationkey').median 
gsample =    proj2.groupby('c_nationkey').sample 

ggmaxi =  proj2.groupby(['c_nationkey', 'c_mktsegment']).max
ggmean =  proj2.groupby(['c_nationkey', 'c_mktsegment']).mean   
ggmini =  proj2.groupby(['c_nationkey', 'c_mktsegment']).min    
ggsumi =  proj2.groupby(['c_nationkey', 'c_mktsegment']).sum    
ggstd =   proj2.groupby(['c_nationkey', 'c_mktsegment']).std    
ggvar =   proj2.groupby(['c_nationkey', 'c_mktsegment']).var    
ggmode =  proj2.groupby(['c_nationkey', 'c_mktsegment']).mode   
ggmedian =proj2.groupby(['c_nationkey', 'c_mktsegment']).median 
ggsample =proj2.groupby(['c_nationkey', 'c_mktsegment']).sample 

print(f'{maxi=}')
print(f'{mean=}')
print(f'{mini=}')
print(f'{sumi=}')
print(f'{std=}')
print(f'{var=}')
print(f'{mode=}')
print(f'{median=}')
print(f'{sample=}')

print(f'{gmaxi=}')
print(f'{gmean=}')
print(f'{gmini=}')
print(f'{gsumi=}')
print(f'{gstd=}')
print(f'{gvar=}')
print(f'{gmode=}')
print(f'{gmedian=}')
print(f'{gsample=}')

print(f'{ggmaxi=}')
print(f'{ggmean=}')
print(f'{ggmini=}')
print(f'{ggsumi=}')
print(f'{ggstd=}')
print(f'{ggvar=}')
print(f'{ggmode=}')
print(f'{ggmedian=}')
print(f'{ggsample=}')
