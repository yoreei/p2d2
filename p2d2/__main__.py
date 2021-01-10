#!/usr/bin/env python3
import pandas
import timeit

from . import argparse_factory
from . import astpp
from . import optimizer

def bench(bytecode):
    return timeit.timeit(lambda: exec(bytecode), number=5)

if __name__ == "__main__":
    args = argparse_factory.parse_args()
    report = pandas.DataFrame(columns=['wflow', 'time_unopt', 'time_opt'])
    #TODO if path is directory:
    # iterate on files inside
    # else:
    with open(args.filepath, "r") as source_file:
        source = source_file.read()

    optimized_bcode = optimizer.optimize(source)
    unoptimized_bcode = compile(source, args.filepath, 'exec')
    
    time_opt = bench(optimized_bcode)
    time_unopt = bench(unoptimized_bcode)
    report.loc[len(report)] = [args.filepath,time_unopt,time_opt]
    
    print(report)
    
    

#TODO Use a profile to detect which parts take the most time
