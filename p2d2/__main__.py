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

C_TIMES = 2
#ADDON_FACTORS = ['ver', 'scale', 'index', 'net']


def warm_up(bytecode, times):
    for _ in range(times):
        exec(bytecode)

ver_list=['p2d2.optimizer', 'p2d2.optimizer1']
def ver(parsetree, nextf):
    global optimizer
    res_df=pandas.DataFrame()
    for ver in ver_list:
        optimizer = importlib.import_module(ver)

        subres_df = nextf(parsetree)
        subres_df['ver']=ver
        res_df=res_df.append(subres_df)

def scale(parsetree, nextf):
    pgbouncer_ini_template='
[databases]
tpch = host=localhost dbname=tpch{}
'
    res_df=pandas.DataFrame()

    for scale_num in [1,10,100]
        pgbouncer_ini=pgbouncer_ini_template.format(scale_num)
        with open('pgbouncer.ini', 'w') as pgbouncer_ini_file:
            pgbouncer_ini_file.write(pgbouncer_ini)
        sts = subprocess.Popen(["/usr/bin/sudo", 'service', 'pgbouncer', 'restart'], shell=False).wait()
        assert sts==0
        
        subres_df = nextf(parsetree)
        subres_df['scale']=scale_num
        res_df=res_df.append(subres_df)
        
    return res_df
        

def index(parsetree, nextf):
    def get_connstr(parsetree):
        for node in parsetree.body:
            if type(node) == ast.Assign and\
            type(node.value)== ast.Call and\
            type(node.value.func)==ast.Attribute and\
            node.value.func.attr == 'connect' and\
            type(node.value.func.value)==ast.Name and\
            node.value.func.value.id=='psychopg2':
                return node.value.args[0].value

    toggle_index_template="""
UPDATE pg_index
SET indisready={}
WHERE indrelid = (
    SELECT oid
    FROM pg_class
);
"""
    res_df = pandas.DataFrame()
    for state in ['true', 'false']:
        toggle_index=toggle_index_template.format(state)

        conn = psycopg2.connect('host=localhost dbname=tpch user=p2d2 password=p2d2')
        cur = conn.cursor()
        cur.execute(toggle_index)
        sql_return = cur.fetchall() # nested like [('c_custkey'),('c_acctbal)]
        cur.close()
        conn.close()
        print('test sql_return')
        breakpoint()
        #assert sql_return

        bool_state = True if state=='true' else False
        subres_df = nextf(parsetree)
        subres_df['index']=bool_state
        res_df=res_df.append(subres_df)
        
    return res_df

def net(parsetree, nextf):
    print('net')
    pass

ADDON_FACTORS = [scale]
#TODO test bench_all, add crosstab, aggregations and many files
def bench_all(parsetree, connstr):
    for factor in ADDON_FACTORS:
        factor(parsetree, basic_bench)
    
    return basic_bench(parsetree)


def basic_bench(parsetree):
    #dep_vars= ['wall_time', 'cpu_utilization', 'mem_usage_db', 'mem_usage_py', 'net_usage']
    def optimize_run(parsetree):
        exec(compile(optimizer.optimize(parsetree), 'str', 'exec')),
        return

    time_incl=[]
    for i in range(C_TIMES):
        time_incl += [{
            'opt': 'incl',
            'rep': i,
            'wall_time': timeit.timeit(lambda: optimize_run(parsetree), number=1),
             'cpu_utilization':0,
             'mem_usage_db':0,
             'mem_usage_py':0,
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
             'mem_usage_db':0,
             'mem_usage_py':0,
             'net_usage':0,
            }]

    return pandas.DataFrame(time_incl+time_excl)

if __name__ == "__main__":
    args = argparse_factory.parse_args()
    #TODO if path is directory:
    # iterate on files inside
    # else:
    with open(args.filepath, "r") as source_file:
        parsetree = ast.parse(source_file.read())

    connstr = get_connstr(parsetree)
    report = bench_all(parsetree, connstr)
    
    print(report)
