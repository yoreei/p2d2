#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
import random

class Dep_var:
    def __init__(self):
        self.mod=1
    def get(self):
        return random.random()*self.mod
    
wall_time=Dep_var()
mem_usage=Dep_var()
net_usage=Dep_var()


# In[2]:




def ver(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df=pandas.DataFrame()
    for module in [('p2d2.optimizer',1), ('p2d2.no_optimizer',1.5)]:
        wall_time.mod*=module[1]
        subres_df = nextf(parsetree, nextlist[:])
        wall_time.mod/=module[1]
        subres_df['ver']=module[0]
        res_df=res_df.append(subres_df)
    return res_df

def scale(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df=pandas.DataFrame()

    for scale_num in [1,10,100]:
        wall_time.mod*=scale_num
        mem_usage.mod*=scale_num
        net_usage.mod*=scale_num

        subres_df = nextf(parsetree, nextlist[:])

        wall_time.mod/=scale_num
        mem_usage.mod/=scale_num
        net_usage.mod/=scale_num

        subres_df['scale']=scale_num
        res_df=res_df.append(subres_df)

    return res_df


def index(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df = pandas.DataFrame()
    for state in [('true',0.76), ('false',1)]:
        wall_time.mod*=state[1]
        subres_df = nextf(parsetree, nextlist[:])
        wall_time.mod/=state[1]
        subres_df['index']=state[0]
        res_df=res_df.append(subres_df)

    return res_df

def net(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df = pandas.DataFrame()
    for area in [('loc',1), ('lan',1.79), ('wan',5.12)]:
        wall_time.mod*=area[1]
        subres_df = nextf(parsetree, nextlist[:])
        wall_time.mod/=area[1]
        subres_df['net']=area[0]
        res_df=res_df.append(subres_df)

    return res_df

def basic_bench(parsetree, nextlist):
    time_incl=[]
    for i in range(10):
        time_incl += [{
            'opt': 'incl',
            'rep': i,
            'wall_time': wall_time.get()+random.random()*2,
             'mem_usage':mem_usage.get(),
             'net_usage':net_usage.get(),
            }]

    time_excl=[]
    for i in range(10):
        time_excl += [{
            'opt': 'excl',
            'rep': i,
            'wall_time': wall_time.get(),
             'mem_usage':mem_usage.get(),
             'net_usage':net_usage.get(),
            }]

    return pandas.DataFrame(time_incl+time_excl)

def bench_all(parsetree, nextlist):
    return nextlist.pop()(parsetree, nextlist)


# In[3]:


ideal = bench_all(None, [basic_bench, ver, scale, index, net])
ideal.to_csv('ideal.csv', index=False)


# In[4]:


wall_time.mod*=5
mem_usage.mod*=5
net_usage.mod*=5
kaggle = bench_all(None, [basic_bench, ver, scale, index, net])
kaggle.to_csv('kaggle.csv', index=False)


# In[ ]:




