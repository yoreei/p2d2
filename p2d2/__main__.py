#!/usr/bin/env python3
import subprocess
import functools
import importlib
import timeit
import ast

import pandas
import psycopg2

from . import argparse_factory
from . import optimizer
from .astpp import *
from . import astpdb

C_TIMES = 2
CONNSTRTEMPLATE='host=localhost dbname=tpch{} user=postgres password=postgres'
CONNSTR=CONNSTRTEMPLATE.format(1)
def shape_traffic(area:str):

    child = subprocess.Popen(['/bin/bash',
         f'/vagrant/net/{area}.sh'])
    child.communicate()
    rc = child.returncode
    assert (rc==0)
    return rc

def exec_sql(query):
        conn = psycopg2.connect(CONNSTR)
        cur = conn.cursor()
        cur.execute(query)
        try:
            db_return = cur.fetchall() # nested: [('c_custkey'),('c_acctbal)]
        except psycopg2.ProgrammingError: #if no results
            db_return=0
        cur.close()
        conn.close()
        return db_return

def change_conn(parsetree, newconn):
    for node in parsetree.body:
        if type(node) == ast.Assign and\
        type(node.value)== ast.Call and\
        type(node.value.func)==ast.Attribute and\
        node.value.func.attr == 'connect' and\
        type(node.value.func.value)==ast.Name and\
        node.value.func.value.id=='psycopg2':
            print('got it')
            node.value.args[0].values[0].value=newconn
    return parsetree

def warm_up(bytecode, times):
    for _ in range(times):
        exec(bytecode)

def ver(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df=pandas.DataFrame()
    global optimizer
    res_df=pandas.DataFrame()
    for ver in ['p2d2.optimizer', 'p2d2.no_optimizer']:
        print(f'ver {ver}')

        optimizer = importlib.import_module(ver)

        subres_df = nextf(parsetree, nextlist[:])

        subres_df['ver']=ver
        res_df=res_df.append(subres_df)

    return res_df

def scale(parsetree, nextlist):

    nextf=nextlist.pop()
    res_df=pandas.DataFrame()

    for scale_num in [1,10]:
        print(f'**scale {scale_num}')

        CONNSTR=CONNSTRTEMPLATE.format(scale_num)
        parsetree=change_conn(parsetree, CONNSTR)
        subres_df = nextf(parsetree, nextlist[:])
        subres_df['scale']=scale_num
        res_df=res_df.append(subres_df)

    return res_df


def index(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df = pandas.DataFrame()

    for state in ['true', 'false']:
        print(f'**index {state}')
        db_return=exec_sql(f'call set_indexes({state});')

        subres_df = nextf(parsetree, nextlist[:])
        subres_df['index']=state
        res_df=res_df.append(subres_df)

    return res_df


def net(parsetree, nextlist):
    nextf=nextlist.pop()
    res_df = pandas.DataFrame()
    # reset any rules before starting
    shape_traffic('loc')
    for area in ['lan', 'wan', 'loc']:
        print(f'**{area}')
        
        shape_traffic(area)
        subres_df = nextf(parsetree, nextlist[:])
        subres_df['net']=area
        res_df=res_df.append(subres_df)

    return res_df

def basic_bench(parsetree, nextlist):
    def optimize_run(parsetree):
        opt_parsetree = optimizer.optimize(parsetree)
        opt_bcode = compile(opt_parsetree, 'str', 'exec')
        exec(opt_bcode)
        return

    #breakpoint()
    time_incl=[]
    for i in range(C_TIMES):
        time_incl += [{
            'opt': 'incl',
            'rep': i,
            'wall_time': timeit.timeit(lambda: optimize_run(parsetree), number=1),
             'cpu_utilization':0,
             'mem_usage':0,
             'net_usage':0,
            }]

    time_excl=[]
    opt_parsetree = optimizer.optimize(parsetree)
    opt_bcode = compile(opt_parsetree, 'str', 'exec')
    for i in range(C_TIMES):
        time_excl += [{
            'opt': 'excl',
            'rep': i,
            'wall_time': timeit.timeit(lambda: exec(opt_bcode), number=1),
             'cpu_utilization':0,
             'mem_usage':0,
             'net_usage':0,
            }]

    return pandas.DataFrame(time_incl+time_excl)

def bench_all(parsetree, nextlist):
    return nextlist.pop()(parsetree, nextlist)

if __name__ == "__main__":
    args = argparse_factory.parse_args()
    #TODO if path is directory:
    # iterate on files inside
    # else:
    with open(args.filepath, "r") as source_file:
        parsetree = ast.parse(source_file.read())

    report = bench_all(parsetree, [basic_bench, ver, index, net, scale])
    
    report.to_csv('/vagrant/docs/bench_results.csv', index=False)
    print(report)
