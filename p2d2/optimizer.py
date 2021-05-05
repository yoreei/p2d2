#!/usr/bin/env python3

import astroid
#if __name__=='__main__':
#    import desugar
#else:
#    from . import desugar
from .desugar import desugar

def inference():
    with open('/vagrant/p2d2/infer/dataframe.pyi') as interface_file:
        interface_parsed = astroid.parse(interface_file.read())
    astroid.register_module_extender(astroid.MANAGER, "pandas", lambda x=interface_parsed: x)
    
def optimize(parsed):
    calls = parsed.nodes_of_class(astroid.node_classes.Call)
    return ""
        

if __name__=='__main__':
    
    code="""
import pandas # 0
import psycopg2 # 1
conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2") # 2
def action(name): # 3
    return None
a = pandas.read_sql_table("lineitem", conn) # 4
b = a['l_custid'] # 5
c = b.head(5) # 6
a = pandas.DataFrame() # 7
b = a['l_custid'] # 8
c = b.head(5) # 9
#mask = a.loc[:, "l_discount"] <= 0.05  # roughly in the middle
l=list(reversed([1,2,3]))

sel = a.loc[mask]

action(sel)
"""
    desugar(code)
    inference()
    parsed = astroid.parse(code)

    #optimize(parsed)
    inferred = parsed.body[6].value.inferred()[0]
    breakpoint()

    #print (list(parsed.body[10].value.infer()))
