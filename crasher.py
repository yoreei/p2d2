import multiprocessing as mp
import numpy
import psutil
import pandas as pd

def foo():
    a=[]
    while True:
       a+=[numpy.ones((1_000_000,))]


class Monitor:
    def available(self):
        return psutil.virtual_memory().available
    def __init__(self):
        self.start_mem=self.available()
        self.diffs=[]
    def check(self):
        mem=self.start_mem-self.available()
        print(mem)
        self.diffs+=[mem]
    def report(self):
        return pd.Series(self.diffs)
        
        
        

if __name__ == '__main__':
    mp.set_start_method('spawn')
    p = mp.Process(target=foo)
    mon = Monitor()
    p.start()
    while p.exitcode==None:
        mon.check()
        p.join(0.01)
    print(mon.report())
    print(f'{p.exitcode=}')
