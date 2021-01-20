#!/usr/bin/env python3
import pandas
import timeit
import ast

from . import argparse_factory
from . import optimizer

def get_connstr(parsetree):
    for node in parsetree.body:
        if type(node) == ast.Assign and\
        type(node.value)== ast.Call and\
        type(node.value.func)==ast.Attribute and\
        node.value.func.attr == 'connect' and\
        type(node.value.func.value)==ast.Name and\
        node.value.func.value.id=='psychopg2':
            return node.value.args[0].value

def drop_caches():
    pass
def warm_up(bytecode, times):
    for _ in range(times):
        exec(bytecode)

def disable_index():
    """
UPDATE pg_index
SET indisready=false
WHERE indrelid = (
    SELECT oid
    FROM pg_class
);
"""
    pass
def enable_index():
    pass

def stopwatch_noopt():
    return timeit.timeit(timeit_run, number=1)
def stopwatch_opt():
    pass

def skip():
    return None
 
#pre_once_l=[warm_up, no_warm_up]
#pre_every_l=[drop_caches, no_drop_cache]
#stopwatch_l=[stopwatch_opt, stopwatch_noopt]

#TODO test bench_all, add crosstab, aggregations and many files
def bench_all(bytecode, times, bench_df):
    pre_once_l=['warm_up', 'no_warm_up']
    pre_every_l=['drop_caches', 'no_drop_cache']
    stopwatch_l=['stopwatch_opt', 'stopwatch_noopt']

    benchmark_ll=[pre_once_l, pre_every_l, stopwatch_l]
    index = pd.MultiIndex.from_product(index)
    benchmark_df = pd.DataFrame(columns=index)

    new_row={}
    for col_tuple in benchmark_df.columns.values: #('a','B','1')
        pre_once=col_tuple[0]
        pre_every=col_tuple[1]
        stopwatch=col_tuple[2]
        
        time_l = bench_factory(bytecode, times, pre_once, pre_every, stopwatch)
        time_series = pd.Series(time_l)
        new_col={col_tuple:time_series}
        
        benchmark_df = benchmark_df.append(new_col, ignore_index=True)
        

def bench_factory(bytecode, times, pre_once, pre_every, stopwatch):
    pre_once()
    time_l=[]
    for _ in range(times):
        pre_every()
        time_l += [stopwatch()]
    return time_l

if __name__ == "__main__":
    args = argparse_factory.parse_args()
    report = pandas.DataFrame(columns=['wflow', 'time_unopt', 'time_opt'])
    #TODO if path is directory:
    # iterate on files inside
    # else:
    with open(args.filepath, "r") as source_file:
        parsetree = ast.parse(source_file.read())

    connstr = get_connstr(parsetree)

    opt_parsetree = optimizer.optimize(parsetree)

    opt_bcode = compile(opt_parsetree, args.filepath, 'exec')
    bcode = compile(parsetree, args.filepath, 'exec')
    
    time_opt = bench(opt_parsetree, 5)
    print('-----------OPTIMIZED DONE, RUNNING UNOPTIMIZED-----')
    time_unopt = bench(bcode, 5)
    report.loc[len(report)] = [args.filepath,time_unopt,time_opt]
    
    print(report)
    
    

#TODO Use a profile to detect which parts take the most time
