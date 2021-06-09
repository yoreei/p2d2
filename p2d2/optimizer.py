#!/usr/bin/env python3

import astroid
#if __name__=='__main__':
#    import desugar
#else:
#    from . import desugar
from .infer import inference
from .preprocessor import preprocess
from .IRBuilder.classifier import Classifier
from .IRBuilder import code_traverser

    
def optimize(raw_code:str, conn_info:str)->str:
    """The main entry point to the optimizer. This activates the whole pipeline as seen on the overview diagram. 
    Input: code read from file
    Output: The optimized, ready-to-run version of the code
    """
    raw_code = p2d2_setup(raw_code, conn_info)
    code:str = preprocess(raw_code)    
    ast:astroid.Module = astroid.parse(code)
    ast.last_p2d2_node = 3
    eagerfiable:set = code_traverser.lazify(ast)
    code_traverser.eagerfy(ast, eagerfiable)
    return ast.as_string() # Python code from AST

def p2d2_setup(code:str, conn_info:str) -> None:
    """
    Our optimizer depends on a few libraries (psychopg2 and pandas) 
    """
    code = f"""import pandas
    import psycopg2
    conn = psycopg2.connect({conn_info})
    cur = conn.cursor()
    """ + code
    return code
    
    
        

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
